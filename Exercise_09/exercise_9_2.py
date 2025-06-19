import arcpy
import arcpy.analysis
# set workspace
arcpy.env.workspace = r'C:\Users\kgttbran\Desktop\Studium\Repo\Python_QGIS_ArcGIS\Exercise_09\exercise_arcpy_1.gdb'
#acces active_assets fc
assets = "active_assets"
#add field which will be the input for the buffer distance
arcpy.management.AddField(assets, "buffer_distance", "TEXT")

#function to calculate the buffer distance
codeblock = """
def calc_buffer_distance(type):
    if type == "mast":
        return "300 Meters"
    if type == "mobile_antenna":
        return "50 Meters"
    else:
        return '100 Meters'"""

#retrive the buffer distance depending on type
expression = "calc_buffer_distance(!type!)"
#calcualte Field
arcpy.management.CalculateField(assets, "buffer_distance", expression,"PYTHON3", codeblock)

#create buffer based on buffer_distance         
arcpy.analysis.Buffer(assets,"coverage","buffer_distance")