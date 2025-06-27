# exercise 10.1
import arcpy
import os

# allow overwriting
arcpy.env.overwriteOutput = True

# set workspace (ADD OWN WORKSPACE HERE)
arcpy.env.workspace = r"C:\Users\kgttbran\Desktop\Studium\Repo\Python_QGIS_ArcGIS\Exercise_10\arcpy_2.gdb"

# path to bus stops
bs_path_assets = os.path.join(arcpy.env.workspace, "stops_ms_mitte")
# path to input (needs to be hardcoded as FC in gdb)
input_path = os.path.join(arcpy.env.workspace, "input")

# run Near tool
arcpy.analysis.Near(
    in_features="input",
    near_features="stops_ms_mitte",
    search_radius=None,
    location="NO_LOCATION",
    angle="NO_ANGLE",
    method="GEODESIC",
    field_names="NEAR_FID NEAR_FID;NEAR_DIST NEAR_DIST",
    distance_unit="Meters"
)

# create dictionary of bus stops with their OBJECTID as key and name as value
bus_stops = { row[0]: row[1] for row in arcpy.da.SearchCursor(bs_path_assets, ["OBJECTID", "name"]) }

# create empty list of results
results = []

# search cursor on input point to search for nearest bus stop
with arcpy.da.SearchCursor(input_path, ["NEAR_FID", "NEAR_DIST"]) as cursor:
    # iterate through bus stops
    for near_fid, near_dist in cursor:
        # if exists, add bus stop name and distance to results list in dictionary, round distance
        if near_fid in bus_stops:
            results.append({
                "name": bus_stops[near_fid],
                "distance": round(near_dist,2)
            })
# print results
for result in results:
    print(f"Name of nearest bus stop: {result['name']}")
    print(f"Distance to nearest bus stop: {result['distance']} meters")