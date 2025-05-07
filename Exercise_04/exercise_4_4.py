import processing

# processing from qgis python interpreter
result = processing.run("native:countpointsinpolygon", {'POLYGONS':'C:/Users/t.lehmann/iCloudDrive/Studium/Geoinformatik Master/5Electives (10 ECTS)/Python in QGIS and ArcGIS (5 ECTS)/Sample Scripts/Sample Scripts - Session 4 Data Muenster/Muenster_City_Districts.shp','POINTS':'C:/Users/t.lehmann/iCloudDrive/Studium/Geoinformatik Master/5Electives (10 ECTS)/Python in QGIS and ArcGIS (5 ECTS)/Sample Scripts/Sample Scripts - Session 4 Data Muenster/Schools.shp','WEIGHT':'','CLASSFIELD':'','FIELD':'NUMPOINTS','OUTPUT':'TEMPORARY_OUTPUT'})

vectorLayer = result['OUTPUT']
features = vectorLayer.getFeatures()

# console output
for feature in features:
    print(f'{feature.attributes()[3]}: {feature.attributes()[7]}')