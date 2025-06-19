import arcpy
import arcpy.analysis
# set workspace
arcpy.env.workspace = r'C:\Users\t.lehmann\Downloads\exercise_arcpy_1.gdb\exercise_arcpy_1.gdb'
#acces active_assets fc
assets = "active_assets"
#add field which will be the input for the buffer distance
arcpy.management.AddField(assets, "buffer_distance", "TEXT")

#function to calculate the buffer distance
codeblock = """
def buffer_distance(type):
    if type == "mast":
        return "300 meters"
    if type == "mobile_antenna":
        return "50 meters"
    else:
        return '100 meters'"""

#retrive the buffer distance depending on type
expression = "buffer_distance(!type!)"
#calcualte Field
arcpy.management.CalculateField(assets, "buffer_distance", expression,"PYTHON3", codeblock)

#create buffer based on buffer_distance         
arcpy.analysis.Buffer(assets, "coverage", "buffer_distance")