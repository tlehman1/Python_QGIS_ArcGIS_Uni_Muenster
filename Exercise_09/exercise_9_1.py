import arcpy
# set workspace
arcpy.env.workspace = r'C:\Users\t.lehmann\Downloads\exercise_arcpy_1.gdb\exercise_arcpy_1.gdb'
#list all point feature classes, remove active asset fc
fc_list = arcpy.ListFeatureClasses(feature_type='Point')
fc_list.remove('active_assets')
#get needed attribute fields
cursor_fields = ["SHAPE@","status", "Type"]
assets = "active_assets"
#initialize insert cursor
icur = arcpy.da.InsertCursor(assets, cursor_fields)
#iterate over listet features
for fc in fc_list:
    scur = arcpy.da.SearchCursor(in_table=fc,field_names=cursor_fields)
    #initialize searchCursor / if status is active, insert row in active_assets fc
    for row in scur:
        if row[1]=="active":
            icur.insertRow(row)
del icur
print("All Features copied")