import uuid
import tempfile
import argparse

from utils import *


# some arguments
parser = argparse.ArgumentParser()
parser.add_argument('extent', type=str, help='path to extent')
parser.add_argument('--print-only', action='store_true', help='print list of available data')
parser.add_argument('--odir', default='.', help='directory to store tiles')
parser.add_argument('--year', type=str, default='latest', help='specify year data captured')
parser.add_argument('--all-years', action='store_true', help='download all available years between --year and latest')
parser.add_argument('--open-browser', action='store_false', help='open browser i.e. do not run headless')
parser.add_argument('--browser', type=str, default='chrome', help='choose between chrome and firefox')
parser.add_argument('--verbose', action='store_true', help='print something')

#     parser.add_argument('--product', '-p', type=str, default='LIDAR Composite DTM',
#                         help='choose from "LIDAR Composite DSM", "LIDAR Composite DTM", \
#                                           "LIDAR Point Cloud", "LIDAR Tiles DSM", \
#                                           "LIDAR Tiles DTM", "National LIDAR Programme DSM", \
#                                           "National LIDAR Programme DTM", "National LIDAR Programme First Return DSM", \
#                                           "National LIDAR Programme Point Cloud"')
parser.add_argument('--point-cloud', '-pc', action='store_true', help='download point cloud')
parser.add_argument('--national', action='store_true', help='download point cloud')
parser.add_argument('--dsm', action='store_true', help='download dsm')
parser.add_argument('--dtm', action='store_true', help='download dtm')

args = parser.parse_args()
if args.odir: args.odir = os.path.abspath(args.odir)

products = ["LIDAR Tiles DSM", "LIDAR Tiles DTM", "LIDAR Point Cloud", "National LIDAR Programme Point Cloud"]
args.required_products = [p for (p, b) in zip(products, [args.dsm, args.dtm, args.point_cloud, args.national]) if b]
if not any(args.required_products):
    raise Exception('pick one or more products using the --point-cloud, --dsm or --dtm flags')

if args.verbose and args.print_only: print('PRINT ONLY - no data will be downloaded')

# temp directory
args.tmp_d = tempfile.mkdtemp()
args.tmp_n = str(uuid.uuid4())

shp = gp.read_file(args.extent)

if shp.area.values[0] > 561333677 or len(shp.explode(index_parts=True)) > 1:
    if args.verbose: 'input geometry is large and or complex, tiling data.'
    tile_input(shp, args)

if num_vertices(shp) > 1000:  # maximum number of vertics accepted by application
    if args.verbose: print('simplifying to <1000 vertices')
    simp = 10

    while num_vertices(shp) > 1000:
        shp.geometry = shp.simplify(simp)
        simp *= 2

    shp.to_file(os.path.join(args.tmp_d, args.tmp_n + '.shp'))
    args.extent = os.path.join(args.tmp_d, args.tmp_n + '.shp')
    if args.verbose: print('simplified polygon saved to:', os.path.join(args.tmp_d, args.tmp_n + '.shp'))

zipPath = os.path.join(args.odir, args.tmp_n + '.zip')
with ZipFile(zipPath, 'w') as zipObj:
    [zipObj.write(f, os.path.basename(f)) for f in glob.glob(os.path.splitext(args.extent)[0] + '*') if
     not f.endswith('.zip')]
    # [print(f) for f in glob.glob(os.path.splitext(args.extent)[0] + '*') if not f.endswith('.zip')]

if args.verbose: print('zip file saved to:', zipPath)

driver = download_tile(zipPath,
                       print_only=args.print_only,
                       year=args.year,
                       all_years=args.all_years,
                       product_list=args.required_products,
                       download_dir=args.odir,
                       headless=args.open_browser,
                       browser=args.browser,
                       verbose=args.verbose)

if not args.open_browser: driver.close()