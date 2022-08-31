# uk-lidar-program

## About

Python code to bulk download UK Environment Agency LiDAR data

## Usage

1. Open src/main.py
2. Specify your configuration (below)
3. Execute src/main.py

## Configuration in src/main.py

    # HEADLESS = False will open browser visually
    HEADLESS = False
    # Available options are listed below
    DESIRED_PRODUCT_LIST = ['National LIDAR Programme Point Cloud']
    DESIRED_YEAR = '2021'
    # If the desired product is not available for the desired year, download the lastest year instead
    LATEST = True
    OUTPUT_DIR = "../assets/output_tiles"
    # The .shp must be accompanied by its respective .dbf, .shx and .prj files
    AOI_SHP_PATH = "../assets/aoi/large-wrington.shp"

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