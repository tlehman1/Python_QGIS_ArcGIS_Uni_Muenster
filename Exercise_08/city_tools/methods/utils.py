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

class createCityDistrictProfile(QgsProcessingAlgorithm):
    # Constants used to refer to parameters and outputs
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    PDF_OUTPUT = 'PDF_OUTPUT'
    CITY_DISTRICT = 'CITY_DISTRICT'
    SCHOOL_OR_SWIM = 'SCHOOL_OR_SWIM'
    HOMEDIR = os.path.expanduser("~")
    QGIS_CACHE_PATH = rf"{HOMEDIR}\AppData\Local\QGIS\QGIS3\cache"

        
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
    
    def create_pdf_profile(self, feature, output_path):
        """Create PDF profile for a single feature with map image"""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            
            print(f"Creating PDF for district: {feature.attributes()}")
            
            # Create PDF document
            doc = SimpleDocTemplate(output_path, pagesize=A4, 
                              leftMargin=72, rightMargin=72, 
                              topMargin=72, bottomMargin=72)
            styles = getSampleStyleSheet()
            story = []
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=20,
                alignment=1  # Center
            )
            
            info_style = ParagraphStyle(
                'InfoStyle',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=8
            )
            
            # Get feature data
            district_name = "Unknown"
            parent_district = "Unknown"
            
            try:
                if 'Name' in feature.fields().names():
                    district_name = str(feature['Name'])
                if 'P_District' in feature.fields().names():
                    parent_district = str(feature['P_District'])
            except Exception as e:
                print(f"Error getting field data: {e}")
            
            # Calculate area
            try:
                area = feature.geometry().area() / 1000000  # km²
            except Exception as e:
                print(f"Error calculating area: {e}")
                area = 0
            
            # Count features
            print("Counting features...")
            households = self.count_features_in_district("House_Numbers", feature)
            parcels = self.count_features_in_district("Muenster_Parcels", feature)
            schools = self.count_features_in_district("Schools", feature)
            pools = self.count_features_in_district("public_swimming_pools", feature)
            
            print(f"Counts - Households: {households}, Parcels: {parcels}, Schools: {schools}, Pools: {pools}")
            
            # Build PDF content
            story.append(Paragraph(f"City District Profile: {district_name}", title_style))
            story.append(Spacer(1, 30))
            
            # Try to create map image
            print("Creating map image...")
            map_created = False
            try:
                map_image_path = self.create_district_map_simple(feature, district_name)
                if map_image_path:
                    print(f"Map image created: {map_image_path}")
                    # Check if file exists and has reasonable size
                    import os
                    if os.path.exists(map_image_path) and os.path.getsize(map_image_path) > 1000:
                        img = Image(map_image_path, width=5*inch, height=3.5*inch)
                        story.append(img)
                        story.append(Spacer(1, 20))
                        map_created = True
                        print("Map image added to PDF")
                    else:
                        print("Map file too small or doesn't exist")
                else:
                    print("Map image path is None")
            except Exception as e:
                print(f"Error creating/adding map: {e}")
            
            if not map_created:
                story.append(Paragraph("<i>Map image could not be generated</i>", styles['Italic']))
                story.append(Spacer(1, 20))
            
            # Add district information
            story.append(Paragraph(f"<b>District Name:</b> {district_name}", info_style))
            story.append(Paragraph(f"<b>Parent District:</b> {parent_district}", info_style))
            story.append(Paragraph(f"<b>Area:</b> {area:.2f} km²", info_style))
            story.append(Spacer(1, 10))
            
            story.append(Paragraph("<b>Statistics:</b>", styles['Heading2']))
            story.append(Paragraph(f"• Number of Households: {households}", info_style))
            story.append(Paragraph(f"• Number of Parcels: {parcels}", info_style))
            story.append(Paragraph(f"• Number of Schools: {schools}", info_style))
            story.append(Paragraph(f"• Number of Swimming Pools: {pools}", info_style))
            
            # Build PDF
            print("Building PDF...")
            doc.build(story)
            print(f"PDF created successfully: {output_path}")
            
            # Clean up temporary map image
            try:
                if 'map_image_path' in locals() and map_image_path:
                    import os
                    if os.path.exists(map_image_path):
                        os.remove(map_image_path)
                        print("Temporary map file cleaned up")
            except Exception as e:
                print(f"Error cleaning up temp file: {e}")
            
            return True
        
        except Exception as e:
            print(f"Error creating PDF: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def create_district_map_simple(self, feature, district_name):
        """Create a simple map image using canvas screenshot"""
        try:
            print("Starting map creation...")
            from qgis.utils import iface
            from qgis.core import QgsRectangle
            from qgis.PyQt.QtCore import QCoreApplication, QTimer
            import tempfile
            import os
            import time
            
            # Get the map canvas
            canvas = iface.mapCanvas()
            print("Got canvas")
            
            # Get district geometry and extent
            district_geometry = feature.geometry()
            district_extent = district_geometry.boundingBox()
            print(f"District extent: {district_extent}")
            
            # Add buffer around the district
            buffer_x = district_extent.width() * 0.3
            buffer_y = district_extent.height() * 0.3
            buffered_extent = QgsRectangle(
                district_extent.xMinimum() - buffer_x,
                district_extent.yMinimum() - buffer_y,
                district_extent.xMaximum() + buffer_x,
                district_extent.yMaximum() + buffer_y
            )
            print(f"Buffered extent: {buffered_extent}")
            
            # Store current extent
            original_extent = canvas.extent()
            print("Stored original extent")
            
            # Set canvas to district extent
            canvas.setExtent(buffered_extent)
            canvas.refresh()
            print("Set new extent and refreshed")
            
            # Wait for refresh to complete
            for i in range(10):  # Wait up to 1 second
                QCoreApplication.processEvents()
                time.sleep(0.1)
            
            # Create temporary file
            temp_dir = tempfile.gettempdir()
            safe_name = "".join(c for c in district_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            map_image_path = os.path.join(temp_dir, f"district_map_{safe_name}.png")
            print(f"Map will be saved to: {map_image_path}")
            
            # Save canvas as image
            success = canvas.saveAsImage(map_image_path)
            print(f"Canvas save result: {success}")
            
            # Restore original extent immediately
            canvas.setExtent(original_extent)
            canvas.refresh()
            print("Restored original extent")
            
            # Check if file was created
            if os.path.exists(map_image_path):
                file_size = os.path.getsize(map_image_path)
                print(f"Map file created with size: {file_size} bytes")
                if file_size > 1000:  # Reasonable minimum size
                    return map_image_path
                else:
                    print("Map file too small, probably empty")
                    return None
            else:
                print("Map file was not created")
                return None
            
        except Exception as e:
            print(f"Error creating simple district map: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Try to restore original extent in case of error
            try:
                from qgis.utils import iface
                if 'original_extent' in locals():
                    iface.mapCanvas().setExtent(original_extent)
                    iface.mapCanvas().refresh()
            except:
                pass
            
            return None

    def count_features_in_district(self, layer_name, district_feature):
        """Count features within the district"""
        try:
            from qgis.core import QgsProject
            
            layers = QgsProject.instance().mapLayersByName(layer_name)
            if not layers:
                print(f"Layer '{layer_name}' not found")
                return 0
            
            layer = layers[0]
            count = 0
            
            district_geometry = district_feature.geometry()
            
            for feature in layer.getFeatures():
                try:
                    if feature.geometry() and feature.geometry().intersects(district_geometry):
                        count += 1
                except Exception as e:
                    print(f"Error checking intersection for feature in {layer_name}: {e}")
                    continue
        
            print(f"Found {count} features in {layer_name}")
            return count
        
        except Exception as e:
            print(f"Error counting features in {layer_name}: {str(e)}")
            return 0
