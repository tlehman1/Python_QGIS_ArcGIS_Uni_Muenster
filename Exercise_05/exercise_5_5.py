# Reading data: Schools and Districts
schools = QgsProject.instance().mapLayersByName('Schools')[0].getFeatures
district_layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
districts = district_layer.getFeatures()

# Creating emtpy list for names
districts_names = []

# Iteravely fill the name list
for district in districts:
    districts_names.append(district["Name"])

# Initiate a modal window / popup with a dropdown containig the names from the list
parent = iface.mainWindow()
sDistrict, bOk = QInputDialog.getItem(parent, "District Names", "Select District: ",
districts_names)

# Handling cancelation of process
if bOk == False:
    QMessageBox.warning(parent, "Schools", "User cancelled")
else:
    print(sDistrict)
    # Selecting chosen district
    selGeom = district_layer.selectByExpression(f'"Name" LIKE "{sDistrict}"', QgsVectorLayer.SetSelection)
    print(selGeom)
    # Check which schools are contained
    res = selGeom.contains(schools)
    print(res)
