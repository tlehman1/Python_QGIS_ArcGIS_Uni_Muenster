# Import modules
from qgis.core import QgsVectorLayer, QgsProject
from qgis.core import *


# Supply path to qgis install location
#QgsApplication.setPrefixPath("/path/to/qgis/installation", True)

# Path to data and QGIS-project
layer_path = r"C:\Users\Sven Harpering\sciebo\GIS-GK\GIS-GK_WS_23_24\GIS Data\Flughafen Muenchen - Datenlieferung I\WKA_Buffer.shp"
project_path = r"C:\Users\Sven Harpering\meine_zweite_karte.qgz"  # for QGIS version 3+

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