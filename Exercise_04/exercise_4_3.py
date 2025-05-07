# Import modules
from qgis.core import QgsVectorLayer, QgsProject
from qgis.core import *

import os

# Initialize QGIS instance
instPath = "C:/QGIS_3_40_5" # CHANGE THIS
QgsApplication.setPrefixPath(instPath, True)
qgs = QgsApplication([], False)
qgs.initQgis()

# Path to data and QGIS-project
project_path = r"Exercise_04\myFirstProject.qgz"  # for QGIS version 3+

# https://www.tutorialspoint.com/python/os_listdir.htm
# Open a file
path = r"Exercise_04\muenster"
dirs = os.listdir( path )

# initiate QGIS
project = QgsProject.instance()
project.read(project_path)

# Print all the files and directories
for file in dirs:
    # filter only shapes
    if file.endswith(".shp"):
        #create new layer
        layer = QgsVectorLayer(f"{path}/{file}", os.path.basename(file), "ogr")
        if not layer.isValid():
            print("Error loading the layer!")
        else:
            # add layer to project
            project.addMapLayer(layer)
            project.write()
            print(f"{file} added to project\nProject saved successfully!")