from src.tile_scraper import TileScraper

# Configuration
# HEADLESS = False will open browser visually
HEADLESS = False
DESIRED_PRODUCT_LIST = ["National LIDAR Programme Point Cloud"]
DESIRED_YEAR = "2021"
# If the desired product is not available for the desired year, download the lastest year instead
LATEST = True
OUTPUT_DIR = "../assets/output_tiles"
# The .shp must be accompanied by its respective .dbf, .shx and .prj files
AOI_SHP_PATH = "../assets/aoi/large-wrington.shp"

if __name__ == "__main__":

    tile_scraper = TileScraper(
        headless=HEADLESS, output_dir=OUTPUT_DIR, aoi_shp_path=AOI_SHP_PATH
    )

    tile_scraper.open_data_gov_uk()

    tile_scraper.upload_aoi_to_data_gov_uk()

    tile_scraper.list_available_data_gov_uk_products()

    tile_scraper.download_desired_data_gov_uk_product(
        desired_product_list=DESIRED_PRODUCT_LIST,
        desired_year=DESIRED_YEAR,
        latest=LATEST,
    )
