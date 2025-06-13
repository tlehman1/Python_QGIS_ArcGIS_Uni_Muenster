from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                                 QPushButton, QFrame, QScrollArea, QWidget)
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsProject

class QueryDialog(QDialog):
    def __init__(self, feature, parent=None):
        super(QueryDialog, self).__init__(parent)
        self.feature = feature
        self.setWindowTitle("City District Profile")
        self.setFixedSize(500, 400)
        self.setup_ui()
        self.populate_data()
    
    def setup_ui(self):
        """Create the user interface"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("City District Profile")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll_widget = QWidget()
        self.content_layout = QVBoxLayout()
        
        # Labels for data (will be populated later)
        self.label_district_name = QLabel()
        self.label_parent_district = QLabel()
        self.label_area = QLabel()
        self.label_households = QLabel()
        self.label_parcels = QLabel()
        self.label_schools = QLabel()
        self.label_pools = QLabel()
        
        # Style labels
        labels = [self.label_district_name, self.label_parent_district, self.label_area,
                 self.label_households, self.label_parcels, self.label_schools, self.label_pools]
        
        for label in labels:
            label.setStyleSheet("padding: 5px; margin: 2px; background-color: #f0f0f0; border: 1px solid #ccc;")
            label.setWordWrap(True)
            self.content_layout.addWidget(label)
        
        scroll_widget.setLayout(self.content_layout)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # Close button
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        close_layout.addWidget(close_button)
        layout.addLayout(close_layout)
        
        self.setLayout(layout)
    
    def populate_data(self):
        """Populate dialog with feature data"""
        try:
            # District name
            district_name = self.feature['Name'] if 'Name' in self.feature.fields().names() else "Unknown"
            self.label_district_name.setText(f"<b>District:</b> {district_name}")
            
            # Parent district
            parent_district = self.feature['P_District'] if 'P_District' in self.feature.fields().names() else "Unknown"
            self.label_parent_district.setText(f"<b>Parent District:</b> {parent_district}")
            
            # Calculate area in km²
            area = self.feature.geometry().area() / 1000000
            self.label_area.setText(f"<b>Area:</b> {area:.2f} km²")
            
            # Count features in district
            households = self.count_features_in_district("House_Numbers")
            parcels = self.count_features_in_district("Muenster_Parcels") 
            schools = self.count_features_in_district("Schools")
            pools = self.count_features_in_district("public_swimming_pools")
            
            self.label_households.setText(f"<b>Number of Households:</b> {households}")
            self.label_parcels.setText(f"<b>Number of Parcels:</b> {parcels}")
            self.label_schools.setText(f"<b>Number of Schools:</b> {schools}")
            self.label_pools.setText(f"<b>Number of Swimming Pools:</b> {pools}")
            
        except Exception as e:
            self.label_district_name.setText(f"<b>Error loading data:</b> {str(e)}")
    
    def count_features_in_district(self, layer_name):
        """Count features within the district"""
        try:
            layers = QgsProject.instance().mapLayersByName(layer_name)
            if not layers:
                return 0
            
            layer = layers[0]
            count = 0
            
            district_geometry = self.feature.geometry()
            
            for feature in layer.getFeatures():
                if feature.geometry().intersects(district_geometry):
                    count += 1
            
            return count
            
        except Exception as e:
            print(f"Error counting features in {layer_name}: {str(e)}")
            return 0