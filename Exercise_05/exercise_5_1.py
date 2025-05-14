# Reading data: Schools and Districts
schools_layer = QgsProject.instance().mapLayersByName('Schools')[0]
district_layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]

# Creating empty list for district names
districts_names = []

# Iteratively fill the name list
districts = district_layer.getFeatures()
for district in districts:
    districts_names.append(district["Name"])

# Sort district names alphabetically
districts_names.sort()

# Initiate a modal window / popup with a dropdown containing the names from the list
parent = iface.mainWindow()
sDistrict, bOk = QInputDialog.getItem(parent, "District Names", "Select District: ",
                                     districts_names)

# Handling cancelation of process
if bOk == False:
    QMessageBox.warning(parent, "Schools", "User cancelled")
else:
    # Selecting chosen district
    district_layer.selectByExpression(f'"Name" = \'{sDistrict}\'', QgsVectorLayer.SetSelection)
    
    # Get the selected district feature and its geometry
    selected_features = district_layer.selectedFeatures()
    if selected_features:
        selected_district = selected_features[0]
        district_geom = selected_district.geometry()
        
        # Find schools within the selected district
        schools_in_district = []
        schools_to_select = []
        
        # Check each school if it's within the district
        for school in schools_layer.getFeatures():
            school_geom = school.geometry()
            if district_geom.contains(school_geom):
                # Get school name and type
                school_name = school["Name"]
                school_type = school["SchoolType"]
                schools_in_district.append((school_name, school_type, school_geom))
                schools_to_select.append(school.id())
        
        # Sort schools alphabetically
        schools_in_district.sort()
        
        # Get centroid of district to compute distance
        district_centroid = district_geom.centroid()

        # Prepare message for QMessageBox
        message = ""
        for school_name, school_type, school_geom in schools_in_district:
            # Calculate distance to center in km, rounded (no reprojection necessary, both datasets are in EPSG:25832)
            dist_to_centroid = round(school_geom.distance(district_centroid) / 1000, 2)
            # Building message string
            message += f"{school_name}, {school_type}, Distance to center: {dist_to_centroid}km\n\n"
        
         # Select schools in the map and zoom to them
        if schools_to_select:
            # Select all schools in the district
            schools_layer.selectByIds(schools_to_select)
            
            # Zoom to selected schools
            canvas = iface.mapCanvas()
            canvas.zoomToSelected(schools_layer)
        
        # Show information dialog with schools
        if schools_in_district:
            QMessageBox.information(parent, f"Schools in {sDistrict}", message)
        else:
            QMessageBox.information(parent, f"Schools in {sDistrict}", "No schools found in this district.")
            