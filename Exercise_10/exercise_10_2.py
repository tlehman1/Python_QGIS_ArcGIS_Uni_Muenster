# exercise 10.2
"""
Script documentation
- Tool parameters are accessed using arcpy.GetParameter() or 
                                     arcpy.GetParameterAsText()
- Update derived parameter values using arcpy.SetParameter() or
                                        arcpy.SetParameterAsText()
"""
# necessary modules for the task
import arcpy
import os

def script_tool(param0):
    """Script code goes below"""
    
    # allow overwriting
    arcpy.env.overwriteOutput = True
    
    # set workspace (ADD YOUR OWN WORKSPACE HERE!)
    arcpy.env.workspace = r"C:\Users\t.lehmann\Downloads\arcpy_2.gdb\arcpy_2.gdb"
    
    # path to the bus stops
    bs_path_assets = os.path.join(arcpy.env.workspace, "stops_ms_mitte")
        
    # run the Near tool - IMPORTANT: method should be GEODESIC!
    arcpy.analysis.Near(
        in_features=param0,
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
    with arcpy.da.SearchCursor(param0, ["NEAR_FID", "NEAR_DIST"]) as cursor:
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
        arcpy.AddMessage(f"Distance to the nearest bus stop: {result['distance']} meters")
        arcpy.AddMessage(f"Name of the nearest bus stop: {result['name']}")
    return

# check if script is run directly
# get the input parameter and call the script tool based on the input
if __name__ == "__main__":
    param0 = arcpy.GetParameterAsText(0)
    script_tool(param0)
