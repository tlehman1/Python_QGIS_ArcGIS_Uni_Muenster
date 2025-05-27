# Exercise 7.1
"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
# imports
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterEnum,
                       QgsProject,
                       QgsFeatureRequest,
                       QgsMessageLog,
                       Qgis)
from qgis import processing
from qgis.utils import iface
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class createCityDistrictProfile(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    pdf_output = 'PDF_OUTPUT'
    cityDistrict = 'cityDistricts'
    schoolOrSwim = 'schoolOrSwim'
    orderedList = []

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return createCityDistrictProfile()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'createCityDistrictProfile'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Create City District Profile')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Exercise scripts')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'createCityDistrictProfile'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Creates a City District profile and saves it in a pdf file")
        
    def createCityDistrictList(self):

        # Get the layer containing city districts
        districtLayers = QgsProject.instance().mapLayersByName("Muenster_City_Districts")
        districtLayer = districtLayers[0]
        
        # Create a QgsFeatureRequest instance to order by "Name"
        request = QgsFeatureRequest()

        # Definde clause
        nameClause = QgsFeatureRequest.OrderByClause("Name", ascending = True)

        # Set clause
        orderby = QgsFeatureRequest.OrderBy([nameClause])

        # assign orderby to the request
        request.setOrderBy(orderby)

        # create list for the distric names

        # save features ordered by attribute "Name"
        for feature in districtLayer.getFeatures(request):
            self.orderedList.append(feature["Name"])
        
        

    def initAlgorithm(self, config=None):

        # Add a parameter for selecting a city district
        self.createCityDistrictList()
        self.addParameter(
            QgsProcessingParameterEnum(
                self.cityDistrict, 'Select a City District', options=self.orderedList
            )
        )

        # Add a parameter for selecting between schools and swimming pools
        self.addParameter(
            QgsProcessingParameterEnum(
                self.schoolOrSwim, 'Select schools or swimming pools', options=['Schools', 'Public swimming pools'], defaultValue = 'Schools'
            )
        )

        # Add a parameter for the output PDF file
        self.addParameter(
            QgsProcessingParameterFileDestination(
                'PDF_OUTPUT',
                self.tr('Output PDF file'),
                fileFilter='PDF files (*.pdf)'
            )
        ) 
    
    def districtInformation(self, parameters, context, feedback):
        
        parameterList = []

        # Get the selected city district and option (school or pool)
        cityParameter = self.parameterAsString(
            parameters,
            self.cityDistrict,
            context
        )
        
        schoolOrSwimParameter = self.parameterAsString(
            parameters,
            self.schoolOrSwim,
            context
        )
        
        cityDistrictName = self.orderedList[int(cityParameter)]

        # Get the layer containing city districts
        districtLayers = QgsProject.instance().mapLayersByName("Muenster_City_Districts")
        districtLayer = districtLayers[0]

         # Iterate through features in the district layer
        features = districtLayer.getFeatures()     
        for feature in features:
            if feature.attributes()[3] == cityDistrictName:
                
                # Name of the city district
                parameterList.append(cityDistrictName)
                
                #Name of the parent district
                parameterList.append(feature.attributes()[4])

                # Size of the area
                geometry = feature.geometry()
                geometryArea = geometry.area()
                parameterList.append(round(geometryArea, 2))
                
                # Number of households in the district
                house_numbers = QgsProject.instance().mapLayersByName("House_Numbers")
                house_number = house_numbers[0]
                house_features = house_number.getFeatures()
                
                houseCounter = 0
                for house in house_features:
                    houseGeometry = house.geometry()
                    if geometry.contains(houseGeometry):
                        houseCounter = houseCounter + 1
                parameterList.append(houseCounter)
                
                # Number of parcels in the district
                parcels = QgsProject.instance().mapLayersByName("Muenster_Parcels")
                parcel = parcels[0]
                parcel_features = parcel.getFeatures()
                
                parcelCounter = 0
                for p in parcel_features:
                    parcelGeometry = p.geometry()
                    if geometry.intersects(parcelGeometry):
                        parcelCounter = parcelCounter + 1
                parameterList.append(parcelCounter)
              
                # Number of schools or pools in the district
                if int(schoolOrSwimParameter) == 0: # School
                    schools = QgsProject.instance().mapLayersByName("Schools")
                    school = schools[0]
                    school_features = school.getFeatures()
                    
                    schoolCounter = 0
                    for s in school_features:
                        schoolGeometry = s.geometry()
                        if geometry.contains(schoolGeometry):
                            schoolCounter = schoolCounter + 1 
                    parameterList.append(schoolCounter)
                
                else: # Swimming Pool
                    pools = QgsProject.instance().mapLayersByName("public_swimming_pools")
                    pool = pools[0]
                    pool_features = pool.getFeatures()
                
                    poolCounter = 0
                    for sp in pool_features:
                        poolGeometry = sp.geometry()
                        if geometry.contains(poolGeometry):
                            poolCounter = poolCounter + 1
                    parameterList.append(poolCounter) 

                # Adjust map view and save a snapshot
                iface.mapCanvas().setExtent(feature.geometry().boundingBox())
                iface.mapCanvas().refresh()
                time.sleep(5)
                picturePath = 'C:/Users/lucah/OneDrive/Desktop/feature321.png'
                iface.mapCanvas().saveAsImage(picturePath)
                
                # return parameters
                return parameterList, schoolOrSwimParameter, picturePath
        
        
    def createPDF(self, pdf_output, parameters, context, feedback):
        parameterList, schoolOrSwimParameter, picturePath = self.districtInformation(parameters, context, feedback)

        # Create PDF with ReportLab
        c = canvas.Canvas(pdf_output, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Add district information to the PDF
        textDistrictName = "Name of the City District: " + parameterList[0]
        c.drawString(200, 750, textDistrictName)
        textPDistrictName = "Name of the Parent District: " + parameterList[1]
        c.drawString(200, 735, textPDistrictName)
        textAreaSize = "Size of the area of the district: " + str(parameterList[2]) + "m²"
        c.drawString(200, 720, textAreaSize)
        textNumberHouses = "Number of households of the district: " + str(parameterList[3])
        c.drawString(200, 705, textNumberHouses)
        textNumberParcels = "Number of parcels of the district: " + str(parameterList[4])
        c.drawString(200, 690, textNumberParcels)

        # Add school or pool information to the PDF
        if int(schoolOrSwimParameter) == 0:
            if parameterList[5] == 0:
                textNumberSchools = "No schools in this district"
                c.drawString(200, 675, textNumberSchools)
            else:
                textNumberSchools = "Number of schools: " + str(parameterList[5])
                c.drawString(200, 675, textNumberSchools)
        else:
            if parameterList[5] == 0:
                textNumberSchools = "No public swimming pools in this district"
                c.drawString(200, 675, textNumberSchools)
            else:
                textNumberPools = "Number of public swimming pools: " + str(parameterList[5])
                c.drawString(200, 675, textNumberPools)

        # Add map snapshot to the PDF
        x = 100
        y = 300
        width = 400
        height = 300
        c.drawImage(picturePath, x, y, width, height)

        # Save the PDF
        c.save()
    
    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        
        pdf_output = self.parameterAsFileOutput(parameters, 'PDF_OUTPUT', context)
        
        self.createPDF(pdf_output, parameters, context, feedback)