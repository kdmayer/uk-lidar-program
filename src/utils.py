from os.path import dirname
from tqdm.auto import tqdm

import urllib.request
import zipfile
import os


def compress_as_zip(aoi_shp_file_path: str = None):
    aoi_dir = dirname(os.path.abspath(aoi_shp_file_path))

    aoi_name = aoi_shp_file_path.split("/")[-1]
    aoi_name = aoi_name[:-4]

    zip_file_path = os.path.join(aoi_dir, aoi_name + ".zip")

    list_of_aoi_files = []

    for file in os.listdir(aoi_dir):
        if file.split(".")[0] == aoi_name:
            list_of_aoi_files.append(os.path.join(aoi_dir, file))

    with zipfile.ZipFile(zip_file_path, "w") as zipMe:
        [
            zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)
            for file in list_of_aoi_files
        ]

    return zip_file_path


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(file_url, file_path):
    with DownloadProgressBar(
        unit="B", unit_scale=True, miniters=1, desc=file_url.split("/")[-1]
    ) as t:
        urllib.request.urlretrieve(file_url, filename=file_path, reporthook=t.update_to)
