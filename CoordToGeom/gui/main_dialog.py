# -*- coding: utf-8 -*-
"""
Main dialog for Coordinates to Geometry plugin
"""
import os
from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                                QLabel, QTextEdit, QComboBox, QLineEdit, QCheckBox,
                                QGroupBox, QRadioButton, QFileDialog, QTabWidget,
                                QWidget, QMessageBox, QTableWidget, QTableWidgetItem,
                                QHeaderView)
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QFont
from qgis.core import (QgsVectorLayer, QgsProject, QgsWkbTypes, 
                      QgsCoordinateReferenceSystem, Qgis)

from ..core.coordinate_parser import CoordinateParser
from ..core.geometry_creator import GeometryCreator
from ..core.layer_manager import LayerManager
from ..core.file_importer import FileImporter
from ..core.attribute_manager import AttributeManager


class CoordToGeomDialog(QDialog):
    """Main dialog class"""
    
    # Signals
    message_emitted = pyqtSignal(str, Qgis.MessageLevel)
    
    def __init__(self, iface, plugin):
        """Constructor
        
        Args:
            iface: QGIS interface
            plugin: Plugin instance
        """
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.plugin = plugin
        
        # Core components
        self.parser = CoordinateParser()
        self.geometry_creator = GeometryCreator()
        self.layer_manager = LayerManager(iface)
        self.file_importer = FileImporter()
        self.attribute_manager = AttributeManager()
        
        # Connect signals
        self.message_emitted.connect(plugin.message_emitted.emit)
        
        # Setup UI
        self.setupUi()
        self.load_layers()
        
    def setupUi(self):
        """Set up the user interface"""
        self.setWindowTitle("Coordinates to Geometry - Enhanced")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Input tab
        self.input_tab = self._create_input_tab()
        self.tab_widget.addTab(self.input_tab, "Coordinate Input")
        
        # Attributes tab
        self.attributes_tab = self._create_attributes_tab()
        self.tab_widget.addTab(self.attributes_tab, "Attributes")
        
        # Settings tab
        self.settings_tab = self._create_settings_tab()
        self.tab_widget.addTab(self.settings_tab, "Settings")
        
        main_layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.create_btn = QPushButton("Create Geometry")
        self.create_btn.clicked.connect(self.create_geometry)
        self.create_btn.setStyleSheet("QPushButton { font-weight: bold; }")
        button_layout.addWidget(self.create_btn)
        
        self.preview_btn = QPushButton("Preview")
        self.preview_btn.clicked.connect(self.preview_geometry)
        button_layout.addWidget(self.preview_btn)
        
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_btn)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def _create_input_tab(self):
        """Create the input tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Input method selection
        method_group = QGroupBox("Input Method")
        method_layout = QVBoxLayout()
        
        self.manual_radio = QRadioButton("Manual Input")
        self.manual_radio.setChecked(True)
        self.manual_radio.toggled.connect(self._toggle_input_method)
        method_layout.addWidget(self.manual_radio)
        
        self.file_radio = QRadioButton("Import from File")
        self.file_radio.toggled.connect(self._toggle_input_method)
        method_layout.addWidget(self.file_radio)
        
        method_group.setLayout(method_layout)
        layout.addWidget(method_group)
        
        # File import section
        self.file_group = QGroupBox("File Import")
        file_layout = QVBoxLayout()
        
        file_select_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Select a text file...")
        file_select_layout.addWidget(self.file_path)
        
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_file)
        file_select_layout.addWidget(self.browse_btn)
        
        file_layout.addLayout(file_select_layout)
        
        # File format info
        format_label = QLabel("Supported formats:\n"
                            "• B X Y (with IDs)\n"
                            "• X Y (coordinates only)\n"
                            "• X,Y (comma-separated)")
        format_label.setStyleSheet("QLabel { color: #666; font-size: 10pt; }")
        file_layout.addWidget(format_label)
        
        self.file_group.setLayout(file_layout)
        self.file_group.setEnabled(False)
        layout.addWidget(self.file_group)
        
        # Manual input section
        self.manual_group = QGroupBox("Manual Coordinate Input")
        manual_layout = QVBoxLayout()
        
        coord_label = QLabel("Enter coordinates (one pair per line):")
        manual_layout.addWidget(coord_label)
        
        self.coords_input = QTextEdit()
        self.coords_input.setPlaceholderText(
            "Examples:\n"
            "100 200\n"
            "150,250\n"
            "200 200\n\n"
            "Or with IDs:\n"
            "P1 100 200\n"
            "P2 150 250"
        )
        font = QFont("Courier", 10)
        self.coords_input.setFont(font)
        manual_layout.addWidget(self.coords_input)
        
        # Coordinate format options
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Separator:"))
        
        self.separator_combo = QComboBox()
        self.separator_combo.addItems(["Auto-detect", "Space", "Comma", "Tab"])
        format_layout.addWidget(self.separator_combo)
        
        self.has_id_check = QCheckBox("First column is ID")
        format_layout.addWidget(self.has_id_check)
        
        format_layout.addStretch()
        manual_layout.addLayout(format_layout)
        
        self.manual_group.setLayout(manual_layout)
        layout.addWidget(self.manual_group)
        
        widget.setLayout(layout)
        return widget
        
    def _create_attributes_tab(self):
        """Create the attributes tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Attribute table
        layout.addWidget(QLabel("Attribute Fields:"))
        
        self.attr_table = QTableWidget()
        self.attr_table.setColumnCount(3)
        self.attr_table.setHorizontalHeaderLabels(["Field Name", "Type", "Default Value"])
        self.attr_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.attr_table)
        
        # Attribute buttons
        attr_btn_layout = QHBoxLayout()
        
        self.add_attr_btn = QPushButton("Add Field")
        self.add_attr_btn.clicked.connect(self.add_attribute_field)
        attr_btn_layout.addWidget(self.add_attr_btn)
        
        self.remove_attr_btn = QPushButton("Remove Selected")
        self.remove_attr_btn.clicked.connect(self.remove_attribute_field)
        attr_btn_layout.addWidget(self.remove_attr_btn)
        
        self.load_from_layer_btn = QPushButton("Load from Layer")
        self.load_from_layer_btn.clicked.connect(self.load_attributes_from_layer)
        attr_btn_layout.addWidget(self.load_from_layer_btn)
        
        attr_btn_layout.addStretch()
        layout.addLayout(attr_btn_layout)
        
        widget.setLayout(layout)
        return widget
        
    def _create_settings_tab(self):
        """Create the settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Geometry settings
        geom_group = QGroupBox("Geometry Settings")
        geom_layout = QVBoxLayout()
        
        # Geometry type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Geometry Type:"))
        self.geom_type = QComboBox()
        self.geom_type.addItems(["Point", "LineString", "Polygon"])
        type_layout.addWidget(self.geom_type)
        type_layout.addStretch()
        geom_layout.addLayout(type_layout)
        
        # CRS selection
        crs_layout = QHBoxLayout()
        crs_layout.addWidget(QLabel("CRS:"))
        self.crs_selector = QComboBox()
        self.crs_selector.addItems([
            "Project CRS",
            "EPSG:4326 (WGS 84)",
            "EPSG:3857 (Web Mercator)",
            "Custom..."
        ])
        crs_layout.addWidget(self.crs_selector)
        crs_layout.addStretch()
        geom_layout.addLayout(crs_layout)
        
        # Auto-close polygon option
        self.auto_close_polygon = QCheckBox("Auto-close polygons")
        self.auto_close_polygon.setChecked(True)
        geom_layout.addWidget(self.auto_close_polygon)
        
        geom_group.setLayout(geom_layout)
        layout.addWidget(geom_group)
        
        # Layer settings
        layer_group = QGroupBox("Layer Settings")
        layer_layout = QVBoxLayout()
        
        # Target layer selection
        self.new_layer_radio = QRadioButton("Create new layer")
        self.new_layer_radio.setChecked(True)
        self.new_layer_radio.toggled.connect(self._toggle_layer_target)
        layer_layout.addWidget(self.new_layer_radio)
        
        # New layer name
        new_layer_layout = QHBoxLayout()
        new_layer_layout.addWidget(QLabel("Layer name:"))
        self.layer_name = QLineEdit()
        self.layer_name.setPlaceholderText("Enter layer name...")
        new_layer_layout.addWidget(self.layer_name)
        layer_layout.addLayout(new_layer_layout)
        
        self.existing_layer_radio = QRadioButton("Add to existing layer")
        self.existing_layer_radio.toggled.connect(self._toggle_layer_target)
        layer_layout.addWidget(self.existing_layer_radio)
        
        # Existing layer selection
        existing_layer_layout = QHBoxLayout()
        existing_layer_layout.addWidget(QLabel("Target layer:"))
        self.layer_combo = QComboBox()
        self.layer_combo.setEnabled(False)
        existing_layer_layout.addWidget(self.layer_combo)
        layer_layout.addLayout(existing_layer_layout)
        
        # Memory layer option
        self.memory_layer_check = QCheckBox("Create as temporary layer")
        self.memory_layer_check.setChecked(True)
        layer_layout.addWidget(self.memory_layer_check)
        
        layer_group.setLayout(layer_layout)
        layout.addWidget(layer_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
        
    def _toggle_input_method(self):
        """Toggle between manual and file input"""
        is_manual = self.manual_radio.isChecked()
        self.manual_group.setEnabled(is_manual)
        self.file_group.setEnabled(not is_manual)
        
    def _toggle_layer_target(self):
        """Toggle between new and existing layer"""
        is_new = self.new_layer_radio.isChecked()
        self.layer_name.setEnabled(is_new)
        self.layer_combo.setEnabled(not is_new)
        self.memory_layer_check.setEnabled(is_new)
        
    def browse_file(self):
        """Browse for input file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Coordinate File",
            "",
            "Text Files (*.txt *.csv);;All Files (*.*)"
        )
        if filename:
            self.file_path.setText(filename)
            
    def load_layers(self):
        """Load vector layers into combo box"""
        self.layer_combo.clear()
        layers = self.layer_manager.get_vector_layers()
        
        for layer in layers:
            # Only add layers with compatible geometry type
            self.layer_combo.addItem(layer.name(), layer)
            
    def add_attribute_field(self):
        """Add a new attribute field"""
        row = self.attr_table.rowCount()
        self.attr_table.insertRow(row)
        
        # Field name
        self.attr_table.setItem(row, 0, QTableWidgetItem("field_" + str(row + 1)))
        
        # Field type combo
        type_combo = QComboBox()
        type_combo.addItems(["String", "Integer", "Double", "Date"])
        self.attr_table.setCellWidget(row, 1, type_combo)
        
        # Default value
        self.attr_table.setItem(row, 2, QTableWidgetItem(""))
        
    def remove_attribute_field(self):
        """Remove selected attribute field"""
        current_row = self.attr_table.currentRow()
        if current_row >= 0:
            self.attr_table.removeRow(current_row)
            
    def load_attributes_from_layer(self):
        """Load attributes from selected layer"""
        if self.existing_layer_radio.isChecked() and self.layer_combo.currentIndex() >= 0:
            layer = self.layer_combo.currentData()
            if layer:
                self.attribute_manager.load_fields_to_table(layer, self.attr_table)
                
    def clear_all(self):
        """Clear all inputs"""
        self.coords_input.clear()
        self.file_path.clear()
        self.layer_name.clear()
        
    def preview_geometry(self):
        """Preview the geometry"""
        try:
            # Get coordinates
            coordinates = self._get_coordinates()
            if not coordinates:
                return
                
            # Show preview in message
            geom_type = self.geom_type.currentText()
            coord_count = len(coordinates)
            
            preview_msg = f"Preview: {geom_type} with {coord_count} points\n"
            preview_msg += "First few coordinates:\n"
            for i, coord in enumerate(coordinates[:5]):
                preview_msg += f"  {coord['id'] if coord.get('id') else i+1}: ({coord['x']}, {coord['y']})\n"
                
            if coord_count > 5:
                preview_msg += f"  ... and {coord_count - 5} more points"
                
            QMessageBox.information(self, "Geometry Preview", preview_msg)
            
        except Exception as e:
            self.plugin.logger.error(f"Preview error: {str(e)}")
            self.message_emitted.emit(f"Preview error: {str(e)}", Qgis.Warning)
            
    def create_geometry(self):
        """Create geometry from coordinates"""
        try:
            # Validate inputs
            if not self._validate_inputs():
                return
                
            # Get coordinates
            coordinates = self._get_coordinates()
            if not coordinates:
                self.message_emitted.emit("No valid coordinates found", Qgis.Warning)
                return
                
            # Get or create target layer
            layer = self._get_target_layer()
            if not layer:
                return
                
            # Create geometries
            geom_type = self.geom_type.currentText()
            features_created = self.geometry_creator.create_features(
                layer, 
                coordinates, 
                geom_type,
                self.auto_close_polygon.isChecked()
            )
            
            if features_created > 0:
                # Zoom to layer extent
                self.iface.mapCanvas().setExtent(layer.extent())
                self.iface.mapCanvas().refresh()
                
                self.message_emitted.emit(
                    f"Successfully created {features_created} feature(s)", 
                    Qgis.Success
                )
                
                # Clear inputs if successful
                if self.manual_radio.isChecked():
                    self.coords_input.clear()
            else:
                self.message_emitted.emit("No features were created", Qgis.Warning)
                
        except Exception as e:
            self.plugin.logger.error(f"Error creating geometry: {str(e)}")
            self.message_emitted.emit(f"Error: {str(e)}", Qgis.Critical)
            
    def _validate_inputs(self):
        """Validate user inputs"""
        # Check geometry type
        geom_type = self.geom_type.currentText()
        
        # Check layer name for new layers
        if self.new_layer_radio.isChecked():
            layer_name = self.layer_name.text().strip()
            if not layer_name:
                self.message_emitted.emit("Please enter a layer name", Qgis.Warning)
                return False
                
        # Check if existing layer is selected
        if self.existing_layer_radio.isChecked():
            if self.layer_combo.currentIndex() < 0:
                self.message_emitted.emit("Please select a target layer", Qgis.Warning)
                return False
                
        return True
        
    def _get_coordinates(self):
        """Get coordinates from input"""
        if self.manual_radio.isChecked():
            # Get from text input
            text = self.coords_input.toPlainText()
            separator = self._get_separator()
            has_id = self.has_id_check.isChecked()
            
            return self.parser.parse_text(text, separator, has_id)
            
        else:
            # Get from file
            file_path = self.file_path.text()
            if not file_path:
                self.message_emitted.emit("Please select a file", Qgis.Warning)
                return []
                
            return self.file_importer.import_file(file_path)
            
    def _get_separator(self):
        """Get the selected separator"""
        sep_text = self.separator_combo.currentText()
        if sep_text == "Space":
            return " "
        elif sep_text == "Comma":
            return ","
        elif sep_text == "Tab":
            return "\t"
        else:  # Auto-detect
            return None
            
    def _get_target_layer(self):
        """Get or create the target layer"""
        if self.new_layer_radio.isChecked():
            # Create new layer
            layer_name = self.layer_name.text().strip()
            geom_type = self.geom_type.currentText()
            crs = self._get_crs()
            is_memory = self.memory_layer_check.isChecked()
            
            # Get attributes from table
            attributes = self.attribute_manager.get_attributes_from_table(self.attr_table)
            
            return self.layer_manager.create_layer(
                layer_name, 
                geom_type, 
                crs, 
                attributes,
                is_memory
            )
        else:
            # Use existing layer
            return self.layer_combo.currentData()
            
    def _get_crs(self):
        """Get the selected CRS"""
        crs_text = self.crs_selector.currentText()
        
        if "Project CRS" in crs_text:
            return QgsProject.instance().crs()
        elif "4326" in crs_text:
            return QgsCoordinateReferenceSystem("EPSG:4326")
        elif "3857" in crs_text:
            return QgsCoordinateReferenceSystem("EPSG:3857")
        else:
            # Custom CRS dialog would go here
            return QgsProject.instance().crs()