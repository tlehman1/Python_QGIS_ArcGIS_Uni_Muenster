from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                                 QLabel, QMessageBox, QFrame)
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsProject

class CityToolsDialog(QDialog):
    def __init__(self, parent=None):
        super(CityToolsDialog, self).__init__(parent)
        self.setWindowTitle("Muenster City District Tools")
        self.setFixedSize(400, 250)
        self.setup_ui()
    
    def setup_ui(self):
        """Create the user interface"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Muenster City District Tools")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("Please select a city district from the map and choose an action:")
        instructions.setWordWrap(True)
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # Buttons
        button_layout = QVBoxLayout()
        
        self.query_button = QPushButton("Attribute Query")
        self.query_button.setMinimumHeight(40)
        self.query_button.setStyleSheet("QPushButton { font-size: 12px; padding: 5px; }")
        button_layout.addWidget(self.query_button)
        
        self.export_button = QPushButton("Export Functionality")
        self.export_button.setMinimumHeight(40)
        self.export_button.setStyleSheet("QPushButton { font-size: 12px; padding: 5px; }")
        button_layout.addWidget(self.export_button)
        
        layout.addLayout(button_layout)
        
        # Close button
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        close_layout.addWidget(close_button)
        layout.addLayout(close_layout)
        
        self.setLayout(layout)
        
        # Connect buttons
        self.query_button.clicked.connect(self.run_attribute_query)
        self.export_button.clicked.connect(self.run_export_functionality)
    
    def get_selected_features(self):
        """Get selected features from city districts layer"""
        possible_names = ["Muenster_City_Districts", "City_Districts", "districts"]
        
        for name in possible_names:
            layers = QgsProject.instance().mapLayersByName(name)
            if layers:
                layer = layers[0]
                selected_features = layer.selectedFeatures()
                return selected_features, None
        
        return None, "City Districts layer not found. Please load a layer with city districts."
    
    def run_attribute_query(self):
        """Handle attribute query button click"""
        selected_features, error = self.get_selected_features()
        
        if error:
            QMessageBox.warning(self, "Error", error)
            return
            
        if not selected_features:
            QMessageBox.warning(self, "No Selection", 
                              "Please select at least one city district feature.")
            return
            
        if len(selected_features) > 1:
            QMessageBox.warning(self, "Multiple Selection", 
                              "Please select only one feature for attribute query.")
            return
        
        # Open attribute dialog
        try:
            from .query_dialog import QueryDialog
            dialog = QueryDialog(selected_features[0], self)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open query dialog: {e}")
    
    def run_export_functionality(self):
        """Handle export functionality button click"""
        selected_features, error = self.get_selected_features()
        
        if error:
            QMessageBox.warning(self, "Error", error)
            return
            
        if not selected_features:
            QMessageBox.warning(self, "No Selection", 
                              "Please select at least one city district feature.")
            return
        
        # Open export dialog
        try:
            from .export_dialog import ExportDialog
            dialog = ExportDialog(selected_features, self)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open export dialog: {e}")

# Für Kompatibilität mit dem bestehenden Code
class muensterCityDistrictToolsDialog(CityToolsDialog):
    pass