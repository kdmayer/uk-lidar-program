# ea_lidar
Python code to bulk download UK Environment Agency LiDAR data

## Example Usage

    main.py /Users/kevin/Projects/uk-lidar-program/assets/aoi/large_wrington.shp
    --odir
    /Users/kevin/Projects/uk-lidar-program/assets/output_tiles
    --year
    2019
    --all-years
    --open-browser
    --browser
    firefox
    --verbose
    --national

## Original Usage

```
usage: ea_lidar.py [-h] [--print-only] [--odir ODIR] [--year YEAR] [--all-years] [--open-browser] [--browser BROWSER] [--verbose] [--point-cloud] [--dsm] [--dtm] extent

positional arguments:
  extent              path to vector file showing ROI (all commmon formats excepted)

optional arguments:
  -h, --help          show this help message and exit
  --print-only        print list of available data
  --odir ODIR         directory to store tiles
  --year YEAR         specify year data captured
  --all-years         download all available years between --year and latest
  --open-browser      open browser i.e. do not run headless
  --browser BROWSER   choose between chrome and firefox (deffault chrome)
  --verbose           print something
  --point-cloud, -pc  download point cloud
  --dsm               download dsm
  --dtm               download dtm
```
