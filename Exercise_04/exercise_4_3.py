# Import modules
from qgis.core import QgsVectorLayer, QgsProject
from qgis.core import *

import os

# Supply path to qgis install location
#QgsApplication.setPrefixPath("/path/to/qgis/installation", True)

# Path to data and QGIS-project
project_path = "Exercise_04\myFirstProject.qgz"  # for QGIS version 3+

# https://www.tutorialspoint.com/python/os_listdir.htm
# Open a file
path = "Exercise_04\muenster"
dirs = os.listdir( path )

project = QgsProject.instance()
project.read(project_path)

# Print all the files and directories
for file in dirs:
    if file.endswith(".shp"):
        layer = QgsVectorLayer(path + file, file[:-4], "ogr")
        if not layer.isValid():
            print("Error loading the layer!")
        else:
            project.addMapLayer(layer)
            project.write()
            print(f"%{file} added to project\nProject saved successfully!")