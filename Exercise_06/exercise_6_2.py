# Create a map canvas object
mc = iface.mapCanvas()

# Get public_swimming_pools.shp layer in the TOC
layer = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]

# Get Muenster_City_Districts layer
districtLayers = QgsProject.instance().mapLayersByName("Muenster_City_Districts")
districtLayer = districtLayers[0]

# Get fields of the layer
fields = layer.fields()
# print(fields.names())

# Declare provider
provider = layer.dataProvider()

# Column type to search in
field_type = fields.indexOf("Type")

# Start editing the layer, edit buffer
layer.startEditing()

# Update 'Type' field values based on their current value
# change H to Hallenbad and F to Freibad
for feature in layer.getFeatures():
    attribute = feature.attributes()
    attribute_type = attribute[field_type]
    
    # use changeAttributeValues method of the respective provider
    if attribute_type == "H":
        provider.changeAttributeValues({feature.id(): {field_type: "Hallenbad"}})
    elif attribute_type == "F":
        provider.changeAttributeValues({feature.id(): {field_type: "Freibad"}})

# Commit changes to 'Type' field
layer.commitChanges()

# Getting access to the layer's capabilities
# capabilities = provider.capabilitiesString()

# Add a new field 'district', update the fields respectively
# use providers addAttributes
# len has to be 50
district_field = QgsField("district", QVariant.String, len=50)
provider.addAttributes([district_field])
layer.updateFields()

# Start editing the layer again
layer.startEditing()

# Get the index of the new 'district' field
fields = layer.fields()  # Update fields to include the new 'district' field
district_field_id = fields.indexOf("district") # index of district

# check which district each swimming pool is and assign the value to the new field
for district in districtLayer.getFeatures():
    districtGeom = district.geometry()
    districtName = district.attributes()[3]

    for pool in layer.getFeatures():
        poolGeom = pool.geometry()
        # if pool geometry is  in district
        # use providers changeAttribute to process 
        # the field and add the district name for the respective pool id
        if districtGeom.contains(poolGeom):
            provider.changeAttributeValues({pool.id(): {district_field_id: districtName}})

# Commit changes to the layer
layer.commitChanges()