# uk-lidar-program

## About

Python code to bulk download UK Environment Agency LiDAR data

## Setup

After cloning the GitHub repo, navigate into the root directory and [set up the Python environment with conda and poetry](https://felix11h.github.io/notes/ops/poetry.html) by executing:

    conda create python=3.9 -n poetry-uk-lidar
    conda activate poetry-uk-lidar
    poetry env use python
    poetry install

Then, specify your configuration in src/main.py:

    HEADLESS = False
    DESIRED_PRODUCT_LIST = ['National LIDAR Programme Point Cloud']
    DESIRED_YEAR = '2021'
    LATEST = True
    OUTPUT_DIR = <Your_Path>
    AOI_SHP_PATH = <Your_Path>

## Usage

From the project's root directory, execute: 

    poetry run python src/main.py

## Available products

- 'LIDAR Composite DTM'
- 'LIDAR Composite First Return DSM'
- 'LIDAR Composite Last Return DSM'
- 'LIDAR Point Cloud'
- 'LIDAR Tiles DSM'
- 'LIDAR Tiles DTM'
- 'National LIDAR Programme DSM'
- 'National LIDAR Programme DTM'
- 'National LIDAR Programme First Return DSM'
- 'National LIDAR Programme Intensity'
- 'National LIDAR Programme Point Cloud'
- 'National LIDAR Programme VOM'
- 'SurfZone DEM 2019'

<!---
## Original usage

    old_main.py ./assets/aoi/large_wrington.shp
    --odir
    ./assets/output_tiles
    --year
    2019
    --all-years
    --open-browser
    --browser
    firefox
    --verbose
    --national
--->