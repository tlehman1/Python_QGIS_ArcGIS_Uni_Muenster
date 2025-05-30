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
                       QgsVectorLayer,
                       Qgis)
from qgis import processing
from qgis.utils import iface
import time
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from shutil import rmtree

# Import matplotlib for charts
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class createCityDistrictProfile(QgsProcessingAlgorithm):
    """
    This algorithm creates a PDF profile for a selected city district
    with various statistics and a map image.
    """

    # Constants used to refer to parameters and outputs
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    PDF_OUTPUT = 'PDF_OUTPUT'
    CITY_DISTRICT = 'CITY_DISTRICT'
    SCHOOL_OR_SWIM = 'SCHOOL_OR_SWIM'
    QGIS_CACHE_PATH = r"C:\Users\<USERNAME>\AppData\Local\QGIS\QGIS3\cache" # !!!! This needs to be Changed !!!

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return createCityDistrictProfile()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm.
        """
        return 'createcitydistrictprofile'

    def displayName(self):
        """
        Returns the translated algorithm name.
        """
        return self.tr('Create City District Profile')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to.
        """
        return self.tr('Exercise scripts')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to.
        """
        return 'exercisescripts'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm.
        """
        return self.tr("Creates a City District profile and saves it in a PDF file")
        
    def createCityDistrictList(self):
        """
        Creates an alphabetically sorted list of city district names.
        """
        # Get the layer containing city districts
        districtLayers = QgsProject.instance().mapLayersByName("Muenster_City_Districts")
        if not districtLayers:
            return []
            
        districtLayer = districtLayers[0]
        
        # Create a QgsFeatureRequest instance to order by "Name"
        request = QgsFeatureRequest()

        # Define clause
        nameClause = QgsFeatureRequest.OrderByClause("Name", ascending=True)

        # Set clause
        orderby = QgsFeatureRequest.OrderBy([nameClause])

        # Assign orderby to the request
        request.setOrderBy(orderby)

        # Create list for the district names
        orderedList = []

        # Save features ordered by attribute "Name"
        for feature in districtLayer.getFeatures(request):
            orderedList.append(feature["Name"])
        
        return orderedList

    def initAlgorithm(self, config=None):
        """
        Define the inputs and output of the algorithm.
        """
        # Get the sorted list of city districts
        district_list = self.createCityDistrictList()
        
        # Add a parameter for selecting a city district
        self.addParameter(
            QgsProcessingParameterEnum(
                self.CITY_DISTRICT, 
                self.tr('Select a City District'), 
                options=district_list,
                defaultValue=0
            )
        )

        # Add a parameter for selecting between schools and swimming pools
        self.addParameter(
            QgsProcessingParameterEnum(
                self.SCHOOL_OR_SWIM, 
                self.tr('Select schools or swimming pools'), 
                options=['Schools', 'Public swimming pools'], 
                defaultValue=0
            )
        )

        # Add a parameter for the output PDF file
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.PDF_OUTPUT,
                self.tr('Output PDF file'),
                fileFilter='PDF files (*.pdf)'
            )
        )

    def getSelectedDistrictFeature(self, district_name):
        """
        Get the feature for the selected district.
        """
        districtLayers = QgsProject.instance().mapLayersByName("Muenster_City_Districts")
        if not districtLayers:
            return None
            
        districtLayer = districtLayers[0]
        
        # Find the district feature by name
        for feature in districtLayer.getFeatures():
            if feature["Name"] == district_name:
                return feature
        
        return None
    
    def districtInformation(self, parameters, context, feedback):
        """
        Gather all information about the selected district.
        """
        parameterList = []

        # Get the selected city district index and option
        cityParameterIndex = self.parameterAsEnum(
            parameters,
            self.CITY_DISTRICT,
            context
        )
        
        schoolOrSwimParameter = self.parameterAsEnum(
            parameters,
            self.SCHOOL_OR_SWIM,
            context
        )
        
        # Get the district name from the list
        district_list = self.createCityDistrictList()
        if cityParameterIndex >= len(district_list):
            feedback.reportError("Invalid district selection")
            return None, None, None
            
        cityDistrictName = district_list[cityParameterIndex]
        
        # Get the district feature
        district_feature = self.getSelectedDistrictFeature(cityDistrictName)
        if not district_feature:
            feedback.reportError(f"District '{cityDistrictName}' not found")
            return None, None, None

        # Name of the city district
        parameterList.append(cityDistrictName)
        
        # Name of the parent district
        parameterList.append(district_feature["P_District"])

        # Size of the area (calculate using geometry)
        geometry = district_feature.geometry()
        geometryArea = geometry.area()
        parameterList.append(round(geometryArea, 2))
        
        # Number of households in the district
        house_numbers = QgsProject.instance().mapLayersByName("House_Numbers")
        if house_numbers:
            house_number = house_numbers[0]
            house_features = house_number.getFeatures()
            
            houseCounter = 0
            for house in house_features:
                houseGeometry = house.geometry()
                if geometry.contains(houseGeometry):
                    houseCounter += 1
            parameterList.append(houseCounter)
        else:
            parameterList.append(0)
        
        # Number of parcels in the district
        parcels = QgsProject.instance().mapLayersByName("Muenster_Parcels")
        if parcels:
            parcel = parcels[0]
            parcel_features = parcel.getFeatures()
            
            parcelCounter = 0
            for p in parcel_features:
                parcelGeometry = p.geometry()
                if geometry.intersects(parcelGeometry):
                    parcelCounter += 1
            parameterList.append(parcelCounter)
        else:
            parameterList.append(0)
      
        # Number of schools or pools in the district
        if schoolOrSwimParameter == 0:  # Schools
            schools = QgsProject.instance().mapLayersByName("Schools")
            if schools:
                school = schools[0]
                school_features = school.getFeatures()
                
                schoolCounter = 0
                for s in school_features:
                    schoolGeometry = s.geometry()
                    if geometry.contains(schoolGeometry):
                        schoolCounter += 1 
                parameterList.append(schoolCounter)
            else:
                parameterList.append(0)
        
        else:  # Swimming Pools
            pools = QgsProject.instance().mapLayersByName("public_swimming_pools")
            if pools:
                pool = pools[0]
                pool_features = pool.getFeatures()
            
                poolCounter = 0
                for sp in pool_features:
                    poolGeometry = sp.geometry()
                    if geometry.contains(poolGeometry):
                        poolCounter += 1
                parameterList.append(poolCounter)
            else:
                parameterList.append(0)

        # clear caches
        if "<USERNAME>" in self.QGIS_CACHE_PATH:
            raise QgsProcessingException("Please provide a valid QGIS cache path!")
        try:
            rmtree(self.QGIS_CACHE_PATH)
        except:
            feedback.reportError("QGIS Caches could not be cleared. This might lead to unexpected behaviour. Please consider clearing your cache manually. Continue processing without cleared caches.")
        iface.mapCanvas().clearCache()
        iface.mapCanvas().clearExtentHistory()

        # Adjust map view and save a snapshot
        iface.mapCanvas().setExtent(district_feature.geometry().boundingBox())
        iface.mapCanvas().refreshAllLayers()
        iface.mapCanvas().redrawAllLayers()
        time.sleep(5)
        
        # Save image in project directory
        project_path = QgsProject.instance().homePath()
        if project_path:
            picturePath = os.path.join(project_path, 'district_map.png')
        else:
            # Fallback to temp directory
            import tempfile
            picturePath = os.path.join(tempfile.gettempdir(), 'district_map.png')
            
        iface.mapCanvas().saveAsImage(picturePath)
        
        # Return parameters
        return parameterList, schoolOrSwimParameter, picturePath

    def createChart(self, district_name, schoolOrSwimParameter):
        """
        Create a chart showing the distribution of pool or school types.
        """
        if not MATPLOTLIB_AVAILABLE:
            return None
            
        district_feature = self.getSelectedDistrictFeature(district_name)
        if not district_feature:
            return None
            
        geometry = district_feature.geometry()
        type_count = {}
        
        if schoolOrSwimParameter == 0:  # Schools
            schools = QgsProject.instance().mapLayersByName("Schools")
            if schools:
                layer = schools[0]
                field_name = "SchoolType"
                title = "School Types Distribution"
            else:
                return None
        else:  # Pools
            pools = QgsProject.instance().mapLayersByName("public_swimming_pools")
            if pools:
                layer = pools[0]
                field_name = "Type"
                title = "Pool Types Distribution"
            else:
                return None
        
        # Count feature types
        for feature in layer.getFeatures():
            if geometry.contains(feature.geometry()):
                attr_value = feature[field_name]
                if attr_value:
                    if attr_value in type_count:
                        type_count[attr_value] += 1
                    else:
                        type_count[attr_value] = 1
        
        if not type_count:
            return None
            
        # Create chart
        fig, ax = plt.subplots(figsize=(8, 6))
        types = list(type_count.keys())
        counts = list(type_count.values())
        
        ax.bar(types, counts, color='steelblue')
        ax.set_xlabel('Types')
        ax.set_ylabel('Count')
        ax.set_title(title)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save chart
        project_path = QgsProject.instance().homePath()
        if project_path:
            chart_path = os.path.join(project_path, 'type_distribution.png')
        else:
            import tempfile
            chart_path = os.path.join(tempfile.gettempdir(), 'type_distribution.png')
            
        plt.savefig(chart_path)
        plt.close()
        
        return chart_path
        
    def createPDF(self, pdf_output, parameters, context, feedback):
        """
        Create the PDF report with all gathered information.
        """
        parameterList, schoolOrSwimParameter, picturePath = self.districtInformation(parameters, context, feedback)
        
        if parameterList is None:
            return False

        # Create PDF with ReportLab
        c = canvas.Canvas(pdf_output, pagesize=letter)
        width, height = letter
        
        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height - 50, f"City District Profile: {parameterList[0]}")
        
        # District information
        c.setFont("Helvetica", 12)
        y_position = height - 100
        line_height = 20
        
        # Parent District
        c.drawString(100, y_position, f"Parent District: {parameterList[1]}")
        y_position -= line_height
        
        # Area size
        c.drawString(100, y_position, f"Area Size: {parameterList[2]:,.2f} m²")
        y_position -= line_height
        
        # Number of households
        c.drawString(100, y_position, f"Number of Households: {parameterList[3]}")
        y_position -= line_height
        
        # Number of parcels
        c.drawString(100, y_position, f"Number of Parcels: {parameterList[4]}")
        y_position -= line_height
        
        # Schools or pools information
        if schoolOrSwimParameter == 0:
            if parameterList[5] == 0:
                text = "No schools in this district"
            else:
                text = f"Number of Schools: {parameterList[5]}"
        else:
            if parameterList[5] == 0:
                text = "No public swimming pools in this district"
            else:
                text = f"Number of Public Swimming Pools: {parameterList[5]}"
        
        c.drawString(100, y_position, text)
        y_position -= line_height * 2
        
        # Add map image
        if os.path.exists(picturePath):
            c.drawString(100, y_position, "Map:")
            y_position -= 10
            c.drawImage(picturePath, 100, y_position - 300, width=400, height=300)
            y_position -= 320
        
        # Add chart for schools/pools if available
        if MATPLOTLIB_AVAILABLE and parameterList[5] > 0:
            district_list = self.createCityDistrictList()
            cityParameterIndex = self.parameterAsEnum(parameters, self.CITY_DISTRICT, context)
            district_name = district_list[cityParameterIndex]
            
            chart_path = self.createChart(district_name, schoolOrSwimParameter)
            if chart_path and os.path.exists(chart_path):
                # Start new page if needed
                if y_position < 350:
                    c.showPage()
                    y_position = height - 50
                    c.setFont("Helvetica", 12)
                
                c.drawString(100, y_position, "Type Distribution:")
                y_position -= 10
                c.drawImage(chart_path, 100, y_position - 250, width=350, height=250)
        
        # Save the PDF
        c.save()
        
        feedback.pushInfo(f"PDF created successfully: {pdf_output}")
        return True
    
    def processAlgorithm(self, parameters, context, feedback):
        """
        Main processing method.
        """
        pdf_output = self.parameterAsFileOutput(parameters, self.PDF_OUTPUT, context)
        
        # Create the PDF
        success = self.createPDF(pdf_output, parameters, context, feedback)
        
        if success:
            return {self.PDF_OUTPUT: pdf_output}
        else:
            raise QgsProcessingException("Failed to create PDF")