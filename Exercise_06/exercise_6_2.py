# Create map canvas object
mc = iface.mapCanvas()

# Get public_swimming_pools.shp layer
layer = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]

# Get Muenster_City_Districts layer
districtLayers = QgsProject.instance().mapLayersByName("Muenster_City_Districts")
districtLayer = districtLayers[0]

# Get fields of layer
fields = layer.fields()

# Declare provider
provider = layer.dataProvider()

# Column type to search in
field_type = fields.indexOf("Type")

# Start editing the layer, edit buffer
layer.startEditing()

# change H to Hallenbad and F to Freibad in field Type
for feature in layer.getFeatures():
    attribute = feature.attributes()
    attribute_type = attribute[field_type]
    
    if attribute_type == "H":
        provider.changeAttributeValues({feature.id(): {field_type: "Hallenbad"}})
    elif attribute_type == "F":
        provider.changeAttributeValues({feature.id(): {field_type: "Freibad"}})

# Commit changes
layer.commitChanges()

# Add new field 'district' with length 50
district_field = QgsField("district", QVariant.String, len=50)
provider.addAttributes([district_field])
layer.updateFields()

# Editing Layer
layer.startEditing()

# Get index of 'district' field
fields = layer.fields()  # Include district
district_field_id = fields.indexOf("district")

# check district of each swimming pool, assign value to new field
for district in districtLayer.getFeatures():
    districtGeom = district.geometry()
    districtName = district.attributes()[3]

    for pool in layer.getFeatures():
        poolGeom = pool.geometry()
        
        # if pool geometry is in district, add district name for pool id
        if districtGeom.contains(poolGeom):
            provider.changeAttributeValues({pool.id(): {district_field_id: districtName}})

# Commit changes
layer.commitChanges()