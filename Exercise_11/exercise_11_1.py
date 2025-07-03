# exercise 10.2
"""
Script documentation
- Tool parameters are accessed using arcpy.GetParameter() or 
                                     arcpy.GetParameterAsText()
- Update derived parameter values using arcpy.SetParameter() or
                                        arcpy.SetParameterAsText()
"""
# necessary imports
import arcpy
import os
import time

def script_tool(input, eval_data, name_field, name_value):
    """Script code goes below"""
    
    # adding the progressor
    arcpy.SetProgressor(type='step',message='Application Progress',min_range=0, max_range=4,step_value=1)
    time.sleep(0.5)
    # checking that parameters are correct
    arcpy.SetProgressorLabel("Checking the inputs")
    arcpy.SetProgressorPosition(0)
    time.sleep(2)

    # allow overwriting
    arcpy.env.overwriteOutput = True

    # set workspace (ADD OWN WORKSPACE HERE)
    arcpy.env.workspace = r"C:\Users\kgttbran\Desktop\Studium\Repo\Python_QGIS_ArcGIS\Exercise_11\arcpy_2.gdb"

    # Step 1
    arcpy.SetProgressorLabel("Creating temporary layer")
    arcpy.SetProgressorPosition(1)
    time.sleep(2)

    # create Feature Layer
    sql = f"{name_field}='{name_value}'"
    arcpy.AddMessage(f"Filter: {sql}")

    try:
        arcpy.MakeFeatureLayer_management(in_features=eval_data,out_layer='feats_to_eval',where_clause=sql)
    except:
        arcpy.AddError("Filtered Feature Layer could not be created! Please try again")
        
    # Step 3
    arcpy.SetProgressorLabel("Calculating the distance")
    arcpy.SetProgressorPosition(2)
    time.sleep(2)

    # run Near tool
    arcpy.analysis.Near(
        in_features=input,
        near_features="feats_to_eval",
        search_radius=None,
        location="NO_LOCATION",
        angle="NO_ANGLE",
        method="GEODESIC",
        field_names="NEAR_FID NEAR_FID;NEAR_DIST NEAR_DIST",
        distance_unit="Meters"
    )
    
    # create dictionary of bus stops with their OBJECTID as key and name as value
    bus_stops = { row[0]: row[1] for row in arcpy.da.SearchCursor("feats_to_eval", ["OBJECTID", "name"]) }
    
    # create empty list of results
    results = []
    
    # Step 4
    arcpy.SetProgressorLabel("Searching for nearest bust stop")
    arcpy.SetProgressorPosition(3)
    time.sleep(2)

    # search cursor on input point to search for nearest bus stop
    with arcpy.da.SearchCursor(input, ["NEAR_FID", "NEAR_DIST"]) as cursor:
        # iterate through bus stops
        for near_fid, near_dist in cursor:
            # if exists, add bus stop name and distance to results list in dictionary, round distance
            if near_fid in bus_stops:
                results.append({
                    "name": bus_stops[near_fid],
                    "distance": round(near_dist,2)
                })

    # Step 5
    arcpy.SetProgressorLabel("Finishing analysis")
    arcpy.SetProgressorPosition(4)
    time.sleep(2)
    # print results
    for result in results:
        arcpy.AddMessage(f"Name of nearest bus stop: {result['name']}")
        arcpy.AddMessage(f"Distance to nearest bus stop: {result['distance']} meters")
    return

# check if script is run directly
# get input and call script tool based on input
if __name__ == "__main__":
    input = arcpy.GetParameterAsText(0)
    eval_data = arcpy.GetParameterAsText(1)
    name_field = arcpy.GetParameterAsText(2)
    name_value = arcpy.GetParameterAsText(3)
    script_tool(input, eval_data, name_field, name_value)
