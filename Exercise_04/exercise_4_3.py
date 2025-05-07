# Import modules
from qgis.core import QgsVectorLayer, QgsProject
from qgis.core import *


# Supply path to qgis install location
#QgsApplication.setPrefixPath("/path/to/qgis/installation", True)

# Path to data and QGIS-project
layer_path = r"C:\Users\t.lehmann\iCloudDrive\Studium\Geoinformatik Master\5Electives (10 ECTS)\Python in QGIS and ArcGIS (5 ECTS)\Sample Scripts\Sample Scripts - Session 4 Data Muenster"
project_path = r"C:\Users\t.lehmann\iCloudDrive\Studium\Geoinformatik Master\5Electives (10 ECTS)\Python in QGIS and ArcGIS (5 ECTS)\Sample Scripts\Sample Scripts - Session 4 QGIS.qgz"  # for QGIS version 3+

# https://www.tutorialspoint.com/python/os_listdir.htm
# Open a file
path = "/home/TP"
dirs = os.listdir( path )

# Print all the files and directories
for file in dirs:
   print(file)

os.listdir()
# Create layer
layer = QgsVectorLayer(layer_path, "WKA eingeladen", "ogr")

# Check if layer is valid
if not layer.isValid():
    print("Error loading the layer!")
else:
    # Create QGIS instance and "open" the project
    project = QgsProject.instance()
    project.read(project_path)

    # Add layer to project
    project.addMapLayer(layer)

    # Save project
    project.write()

    print("Layer added to project\nProject saved successfully!")