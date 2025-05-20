# Create a memory layer with MultiPolygon geometry type
layer = QgsVectorLayer("MultiPolygon", "temp_standard_land_value_muenster", "memory")

# Set CRS to EPSG:25832 (common for Münster, Germany)
layer.setCrs(QgsCoordinateReferenceSystem("EPSG:25832"))

# Get the data provider for the layer
provider = layer.dataProvider()

# Add the required fields to the layer
provider.addAttributes([
    QgsField("standard_land_value", QVariant.Double),
    QgsField("type", QVariant.String),
    QgsField("district", QVariant.String)
])

# Update the layer's fields
layer.updateFields()

# Open and read the CSV file
with open(r"C:\Users\t.lehmann\Downloads\Data for Session 6\Data for Session 6\standard_land_value_muenster.csv") as csv_file:
    # Skip the header line
    next(csv_file)
    
    # Process each line in the file
    for line in csv_file:
        # Remove the newline character at the end
        line = line.rstrip('\n')
        
        # Split the line by semicolon, but limit to 4 parts
        # to avoid splitting the WKT part which may contain semicolons
        parts = line.split(';', 3)
        
        if len(parts) == 4:
            # Extract the data
            standard_land_value = parts[0]  # No longer converting to float
            land_type = parts[1]
            district = parts[2]
            wkt = parts[3]
            
            # Create a new feature
            feature = QgsFeature()
            
            # Set the feature's geometry from WKT
            geometry = QgsGeometry.fromWkt(wkt)
            feature.setGeometry(geometry)
            
            # Set the feature's attributes
            feature.setAttributes([
                standard_land_value,
                land_type,
                district
            ])
            
            # Add the feature to the layer
            provider.addFeature(feature)

# Update the layer's extent
layer.updateExtents()

# Add the layer to the map
QgsProject.instance().addMapLayer(layer)