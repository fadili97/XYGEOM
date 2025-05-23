# -*- coding: utf-8 -*-
"""
Attribute manager module
Handles attribute table management
"""
from typing import List, Dict
from qgis.core import QgsVectorLayer, QgsField
from qgis.PyQt.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox
from qgis.PyQt.QtCore import QVariant


class AttributeManager:
    """Manage layer attributes and field definitions"""
    
    def __init__(self):
        """Initialize attribute manager"""
        # Field type mapping
        self.field_types = {
            'String': QVariant.String,
            'Integer': QVariant.Int,
            'Double': QVariant.Double,
            'Date': QVariant.Date,
            'DateTime': QVariant.DateTime,
            'Boolean': QVariant.Bool
        }
        
    def get_attributes_from_table(self, table: QTableWidget) -> List[Dict[str, any]]:
        """Extract attribute definitions from table widget
        
        Args:
            table: QTableWidget containing attribute definitions
            
        Returns:
            List of attribute dictionaries
        """
        attributes = []
        
        for row in range(table.rowCount()):
            # Get field name
            name_item = table.item(row, 0)
            if not name_item:
                continue
                
            field_name = name_item.text().strip()
            if not field_name:
                continue
                
            # Get field type
            type_widget = table.cellWidget(row, 1)
            if isinstance(type_widget, QComboBox):
                field_type = type_widget.currentText()
            else:
                field_type = 'String'  # Default
                
            # Get default value
            default_item = table.item(row, 2)
            default_value = default_item.text() if default_item else ''
            
            # Create attribute definition
            attr_def = {
                'name': field_name,
                'type': field_type,
                'default': default_value,
                'length': 255 if field_type == 'String' else 10,
                'precision': 3 if field_type == 'Double' else 0
            }
            
            attributes.append(attr_def)
            
        return attributes
        
    def load_fields_to_table(self, layer: QgsVectorLayer, table: QTableWidget):
        """Load layer fields into table widget
        
        Args:
            layer: Source vector layer
            table: Target table widget
        """
        # Clear existing rows
        table.setRowCount(0)
        
        # Add fields
        for field in layer.fields():
            row = table.rowCount()
            table.insertRow(row)
            
            # Field name
            table.setItem(row, 0, QTableWidgetItem(field.name()))
            
            # Field type
            type_combo = QComboBox()
            type_combo.addItems(list(self.field_types.keys()))
            
            # Map QVariant type to string
            qvar_type = field.type()
            type_str = self._qvariant_to_string(qvar_type)
            
            index = type_combo.findText(type_str)
            if index >= 0:
                type_combo.setCurrentIndex(index)
                
            table.setCellWidget(row, 1, type_combo)
            
            # Default value (empty for existing fields)
            table.setItem(row, 2, QTableWidgetItem(""))
            
    def _qvariant_to_string(self, qvar_type: QVariant.Type) -> str:
        """Convert QVariant type to string representation
        
        Args:
            qvar_type: QVariant type
            
        Returns:
            String type name
        """
        type_map = {
            QVariant.String: 'String',
            QVariant.Int: 'Integer',
            QVariant.LongLong: 'Integer',
            QVariant.Double: 'Double',
            QVariant.Date: 'Date',
            QVariant.DateTime: 'DateTime',
            QVariant.Bool: 'Boolean'
        }
        
        return type_map.get(qvar_type, 'String')
        
    def create_default_attributes(self, geom_type: str) -> List[Dict[str, any]]:
        """Create default attributes based on geometry type
        
        Args:
            geom_type: Geometry type
            
        Returns:
            List of default attribute definitions
        """
        # Common attributes
        attributes = [
            {
                'name': 'id',
                'type': 'String',
                'length': 50,
                'default': ''
            },
            {
                'name': 'name',
                'type': 'String',
                'length': 100,
                'default': ''
            },
            {
                'name': 'description',
                'type': 'String',
                'length': 255,
                'default': ''
            }
        ]
        
        # Geometry-specific attributes
        if geom_type == "Point":
            attributes.extend([
                {
                    'name': 'elevation',
                    'type': 'Double',
                    'precision': 2,
                    'default': '0'
                }
            ])
        elif geom_type == "LineString":
            attributes.extend([
                {
                    'name': 'length',
                    'type': 'Double',
                    'precision': 3,
                    'default': '0'
                }
            ])
        elif geom_type == "Polygon":
            attributes.extend([
                {
                    'name': 'area',
                    'type': 'Double',
                    'precision': 3,
                    'default': '0'
                },
                {
                    'name': 'perimeter',
                    'type': 'Double',
                    'precision': 3,
                    'default': '0'
                }
            ])
            
        return attributes
        
    def validate_field_name(self, name: str, existing_fields: List[str] = None) -> tuple:
        """Validate field name
        
        Args:
            name: Field name to validate
            existing_fields: List of existing field names
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if empty
        if not name or not name.strip():
            return False, "Field name cannot be empty"
            
        # Check length
        if len(name) > 63:  # PostgreSQL limit
            return False, "Field name too long (max 63 characters)"
            
        # Check valid characters (alphanumeric and underscore)
        if not name.replace('_', '').isalnum():
            return False, "Field name can only contain letters, numbers, and underscores"
            
        # Check if starts with number
        if name[0].isdigit():
            return False, "Field name cannot start with a number"
            
        # Check reserved words
        reserved_words = ['id', 'fid', 'geom', 'geometry', 'shape']
        if name.lower() in reserved_words and existing_fields:
            if name.lower() in [f.lower() for f in existing_fields]:
                return False, f"'{name}' is already in use"
                
        # Check duplicates
        if existing_fields and name in existing_fields:
            return False, f"Field '{name}' already exists"
            
        return True, ""