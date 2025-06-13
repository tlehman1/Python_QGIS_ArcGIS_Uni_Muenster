from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                                 QLabel, QFileDialog, QMessageBox, QFrame)
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsProject
import os
import csv

class ExportDialog(QDialog):
    def __init__(self, selected_features, parent=None):
        super(ExportDialog, self).__init__(parent)
        self.selected_features = selected_features
        self.setWindowTitle("Export Options")
        self.setFixedSize(400, 300)
        self.setup_ui()
    
    def setup_ui(self):
        """Create the user interface"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Export Options")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Info
        info_text = f"Selected features: {len(self.selected_features)}"
        info = QLabel(info_text)
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # Export buttons
        button_layout = QVBoxLayout()
        
        self.csv_button = QPushButton("Export as CSV file")
        self.csv_button.setMinimumHeight(50)
        self.csv_button.setStyleSheet("QPushButton { font-size: 12px; padding: 10px; }")
        button_layout.addWidget(self.csv_button)
        
        self.pdf_button = QPushButton("Export as PDF file")
        self.pdf_button.setMinimumHeight(50)
        self.pdf_button.setStyleSheet("QPushButton { font-size: 12px; padding: 10px; }")
        button_layout.addWidget(self.pdf_button)
        
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
        self.csv_button.clicked.connect(self.export_csv)
        self.pdf_button.clicked.connect(self.export_pdf)
    
    def export_csv(self):
        """Export selected features to CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV File", "", "CSV Files (*.csv)")
        
        if not file_path:
            QMessageBox.information(self, "Cancelled", "Export cancelled by user.")
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['District Name', 'Area (km²)', 'Number of Parcels', 'Number of Schools'])
                
                # Write data for each selected feature
                for feature in self.selected_features:
                    name = feature['Name'] if 'Name' in feature.fields().names() else "Unknown"
                    area = feature.geometry().area() / 1000000  # Convert to km²
                    parcels = self.count_features_in_district("Muenster_Parcels", feature)
                    schools = self.count_features_in_district("Schools", feature)
                    
                    writer.writerow([name, f"{area:.2f}", parcels, schools])
            
            QMessageBox.information(self, "Success", f"CSV exported successfully to:\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export CSV:\n{str(e)}")
    
    def export_pdf(self):
        """Export selected feature to PDF"""
        if len(self.selected_features) > 1:
            QMessageBox.warning(self, "Multiple Selection", 
                              "Please select only one feature for PDF export.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF File", "", "PDF Files (*.pdf)")
        
        if not file_path:
            QMessageBox.information(self, "Cancelled", "Export cancelled by user.")
            return
        
        try:
            from .methods.utils import createCityDistrictProfile
            
            # Create processor instance
            processor = createCityDistrictProfile()
            
            # Create PDF profile
            success = processor.create_pdf_profile(self.selected_features[0], file_path)
            
            if success:
                QMessageBox.information(self, "Success", f"PDF exported successfully to:\n{file_path}")
            else:
                QMessageBox.warning(self, "Warning", "PDF creation completed but may have issues.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export PDF:\n{str(e)}")
    
    def count_features_in_district(self, layer_name, district_feature):
        """Count features within the district"""
        try:
            layers = QgsProject.instance().mapLayersByName(layer_name)
            if not layers:
                return 0
            
            layer = layers[0]
            count = 0
            
            district_geometry = district_feature.geometry()
            
            for feature in layer.getFeatures():
                if feature.geometry().intersects(district_geometry):
                    count += 1
            
            return count
            
        except Exception as e:
            print(f"Error counting features in {layer_name}: {str(e)}")
            return 0