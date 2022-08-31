from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
)

from typing import List
from utils import compress_as_zip, download_url

import os


class TileScraper:
    def __init__(
        self, headless: bool = False, output_dir: str = None, aoi_shp_path: str = None
    ):
        """
        Instantiate Firefox browser instance.
        """
        opts = Options()
        opts.headless = headless
        self.browser = Firefox(options=opts)
        self.output_dir = output_dir
        self.aoi_shp_path = aoi_shp_path
        self.aoi_zip_path = compress_as_zip(self.aoi_shp_path)

    def open_data_gov_uk(self):

        print("...waiting for data.gov.uk page to load.")

        self.browser.get(
            "https://environment.data.gov.uk/DefraDataDownload/?Mode=survey"
        )

        self.wait = WebDriverWait(self.browser, 300)

        print("...page has loaded.")

    def upload_aoi_to_data_gov_uk(self):

        print("...waiting for shapefile to load")

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#fileid")))

        self.browser.find_element(by=By.CSS_SELECTOR, value="#fileid").send_keys(
            [self.aoi_zip_path]
        )

        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".grid-item-container"))
        )

        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".grid-item-container"))
        )

        self.E1 = self.browser.find_element(
            by=By.CSS_SELECTOR, value=".grid-item-container"
        )

        print("...shapefile has loaded")

    def list_available_data_gov_uk_products(self):

        print("...waiting for available products to load")

        while True:  # hack :(

            try:
                self.E1.click()

            except ElementNotInteractableException as e:
                break

            self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#productSelect"))
            )

            self.list_of_products = [
                x.get_attribute("value")
                for x in Select(
                    self.browser.find_element(
                        by=By.CSS_SELECTOR, value="#productSelect"
                    )
                ).options
            ]

        print(f"List of products: {self.list_of_products}")

    def download_desired_data_gov_uk_product(
        self,
        desired_product_list: List = None,
        desired_year: str = None,
        latest: bool = True,
    ):

        for desired_product in desired_product_list:

            if desired_product not in self.list_of_products:
                print(f"Desired product: {desired_product} is not available.")
                continue

            else:
                xPath = f'//*[@id="productSelect"]/option[{self.list_of_products.index(desired_product) + 1}]'

                self.wait.until(EC.presence_of_element_located((By.XPATH, xPath)))
                self.browser.find_element(by=By.XPATH, value=xPath).click()

                available_years_list = [
                    x.get_attribute("value")
                    for x in Select(
                        self.browser.find_element(
                            by=By.CSS_SELECTOR, value="#yearSelect"
                        )
                    ).options
                ]

                if desired_year in available_years_list:
                    year_element = [
                        f'//*[@id="yearSelect"]/option[{available_years_list.index(desired_year) + 1}]'
                    ]

                elif (desired_year not in available_years_list) and latest:

                    year_element = ['//*[@id="yearSelect"]/option[1]']

                else:
                    print(f"Desired product is not available.")
                    continue

                year_to_be_downloaded = available_years_list[
                    int(year_element[0].split("[")[-1][:-1]) - 1
                ]

                print(f"Year to be downloaded: {year_to_be_downloaded}")
                print(f"Desired year: {desired_year}")
                print(f"Available years: {available_years_list}")

                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, year_element[0]))
                )
                self.browser.find_element(by=By.XPATH, value=year_element[0]).click()
                link_idx = 1

                while True:
                    try:
                        file_url = self.browser.find_element(
                            by=By.CSS_SELECTOR,
                            value=f".data-ready-container > a:nth-child({link_idx})",
                        ).get_attribute("href")

                        file_path = os.path.join(
                            self.output_dir,
                            self.aoi_zip_path.split("/")[-1][:-4]
                            + "-"
                            + file_url.split("/")[-1],
                        )

                        if os.path.isfile(file_path):
                            print(f"...tile has already been downloaded")

                        else:
                            download_url(file_url, file_path)
                            print(f"Saved tile to {file_path}")

                        link_idx += 1

                    except NoSuchElementException:
                        print(
                            f"{link_idx - 1} files downloaded for {year_to_be_downloaded}"
                        )
                        break
                    except Exception as err:
                        print(err)

        self.browser.close()
