# Getting layer with city districts of Münster
district_layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
districts = district_layer.getFeatures()

# Initialize and call input popup
parent = iface.mainWindow()
sCoords, bOK = QInputDialog.getText(parent, "Coordinates", "Enter coordinates as latitude, longitude", text = "51.96066,7.62476")

# Declaring CRS for later transformation
wgs_crs = QgsCoordinateReferenceSystem(4326)
etrs_crs = QgsCoordinateReferenceSystem(25832)

# Handling cancelation of process
if bOK == False:
    QMessageBox.warning(parent, "Error", "User cancelled")
else:
    # Splitting coordinate string at the comma to get 2 coordinates
    coord_list = sCoords.split(",")

    # Check if input string was correct and resulted in 2 coordinates
    if len(coord_list)!=2:
        QMessageBox.warning(parent, "Error", "Please insert correct coordinates. Use '.' as decimal and ',' as general seperator and only provide one pair of coordinates.")
    else:
        # temp variable to check if the point was within a district
        inside = False

        # temp variable to store the name of the containing district
        matched_district = ""

        # Initializing a transformation object from WGS84 to ETRS89
        transformation = QgsCoordinateTransform(wgs_crs, etrs_crs, QgsProject.instance())

        # Creating an XY WGS84 point from input
        point_xy = QgsPointXY(float(coord_list[1]),float(coord_list[0]))

        # Transforming the point to ETRS89
        point_etrs = transformation.transform(point_xy)

        # Checking if point is in district. If yes, inside is true and the for will stop
        for district in districts:
            if district.geometry().contains(point_etrs):
                inside = True
                matched_district = district["Name"]
                break
        
        # Send message, wheter the point is inside a district or not
        if inside:
            QMessageBox.warning(parent, "You won!", f"The point you submitted is inside the district {matched_district}.")
        else:
            QMessageBox.warning(parent, "You lost!", f"The point you submitted is not inside of a city district of Münster.")