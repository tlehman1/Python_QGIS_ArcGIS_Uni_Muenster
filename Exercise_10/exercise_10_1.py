# exercise 10.1
import arcpy
import os

# allow overwriting
arcpy.env.overwriteOutput = True

# set workspace (ADD YOUR OWN WORKSPACE HERE!)
arcpy.env.workspace = r"C:\Users\t.lehmann\Downloads\arcpy_2.gdb\arcpy_2.gdb"

# path to the bus stops
bs_path_assets = os.path.join(arcpy.env.workspace, "stops_ms_mitte")
# path to input (hardcoded input point for testing purposes)
input_path = os.path.join(arcpy.env.workspace, "input")

# run the Near tool - IMPORTANT: method should be GEODESIC!
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

# create a dictionary of bus stops with their OBJECTID as key and name as value
bus_stops = { row[0]: row[1] for row in arcpy.da.SearchCursor(bs_path_assets, ["OBJECTID", "name"]) }

# create an empty list of results
results = []

# search cursor on the input point to search for the nearest bus stop
with arcpy.da.SearchCursor(input_path, ["NEAR_FID", "NEAR_DIST"]) as cursor:
    # iterate through each row
    for near_fid, near_dist in cursor:
        # if exists, add the bus stop name and distance to the results list in dictionary
        if near_fid in bus_stops:
            results.append({
                "name": bus_stops[near_fid],
                "distance": near_dist
            })
# ultimatly print the results
for result in results:
    print(f"Bus Stop Name: {result['name']}")
    print(f"Distance: {result['distance']}m")