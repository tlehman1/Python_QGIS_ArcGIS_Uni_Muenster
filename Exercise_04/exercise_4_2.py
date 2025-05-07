import csv

# select active layer
layer = iface.activeLayer()

# select features from active layer
features = layer.selectedFeatures()

# set path (need to change)
path = 'C:/Users/t.lehmann/OneDrive - con terra/Desktop/'

# write csv
# https://stackoverflow.com/questions/51972676/how-to-write-to-csv-in-python/51972946
with open(path + 'SchoolsReport.csv', 'w') as csvfile:
    fileout = csv.writer(csvfile, delimiter=';')
    
    # write first line in document
    fileout.writerow(['Name','X','Y'])
    
    # select school features and write it to the .csv file
    for feature in features:
        schoolName = feature.attributes()[1]
        schoolGeom = feature.geometry()
        coordinate = schoolGeom.asPoint()
        x = coordinate.x()
        y = coordinate.y()
        fileout.writerow([schoolName,x,y])
    print('Done')