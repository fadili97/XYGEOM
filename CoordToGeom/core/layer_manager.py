# -*- coding: utf-8 -*-
"""
Layer manager module
Handles layer creation and management
"""
from typing import List, Dict, Optional
from qgis.core import (QgsVectorLayer, QgsProject, QgsWkbTypes, 
                      QgsCoordinateReferenceSystem, QgsField,
                      QgsVectorFileWriter, QgsVectorDataProvider)
from qgis.PyQt.QtCore import QVariant


class LayerManager:
    """Manage vector layers"""
    
    def __init__(self, iface):
        """Initialize with QGIS interface
        
        Args:
            iface: QGIS interface
        """
        self.iface = iface
        
    def get_vector_layers(self, geom_type: Optional[str] = None) -> List[QgsVectorLayer]:
        """Get all vector layers, optionally filtered by geometry type
        
        Args:
            geom_type: Optional geometry type filter
            
        Returns:
            List of vector layers
        """
        layers = []
        
        for layer in QgsProject.instance().mapLayers().values():
            if isinstance(layer, QgsVectorLayer):
                if geom_type:
                    # Filter by geometry type
                    layer_geom_type = QgsWkbTypes.displayString(layer.wkbType())
                    if geom_type.lower() in layer_geom_type.lower():
                        layers.append(layer)
                else:
                    layers.append(layer)
                    
        return layers
        
    def create_layer(self, name: str, geom_type: str, 
                    crs: QgsCoordinateReferenceSystem,
                    attributes: List[Dict[str, any]],
                    is_memory: bool = True) -> QgsVectorLayer:
        """Create a new vector layer
        
        Args:
            name: Layer name
            geom_type: Geometry type
            crs: Coordinate reference system
            attributes: List of attribute definitions
            is_memory: Whether to create memory layer
            
        Returns:
            Created vector layer
        """
        # Build layer URI
        if is_memory:
            uri = self._build_memory_layer_uri(geom_type, crs)
            layer = QgsVectorLayer(uri, name, "memory")
        else:
            # For file-based layers, would need file path
            # This is a placeholder for future implementation
            uri = self._build_memory_layer_uri(geom_type, crs)
            layer = QgsVectorLayer(uri, name, "memory")
            
        if not layer.isValid():
            raise Exception(f"Failed to create layer '{name}'")
            
        # Add attributes
        self._add_attributes_to_layer(layer, attributes)
        
        # Add to project
        QgsProject.instance().addMapLayer(layer)
        
        return layer
        
    def _build_memory_layer_uri(self, geom_type: str, 
                               crs: QgsCoordinateReferenceSystem) -> str:
        """Build URI for memory layer
        
        Args:
            geom_type: Geometry type
            crs: CRS
            
        Returns:
            Layer URI string
        """
        # Map geometry type names to QGIS types
        geom_map = {
            "Point": "Point",
            "LineString": "LineString",
            "Polygon": "Polygon",
            "MultiPoint": "MultiPoint",
            "MultiLineString": "MultiLineString",
            "MultiPolygon": "MultiPolygon"
        }
        
        qgis_geom_type = geom_map.get(geom_type, "Point")
        
        # Build URI
        uri = f"{qgis_geom_type}?crs={crs.authid()}"
        
        # Add default ID field
        uri += "&field=id:string(50)"
        
        return uri
        
    def _add_attributes_to_layer(self, layer: QgsVectorLayer, 
                                attributes: List[Dict[str, any]]):
        """Add attributes to layer
        
        Args:
            layer: Target layer
            attributes: Attribute definitions
        """
        if not attributes:
            return
            
        provider = layer.dataProvider()
        
        # Create QgsField objects
        fields = []
        for attr in attributes:
            field_name = attr.get('name', 'field')
            field_type = attr.get('type', 'String')
            field_length = attr.get('length', 50)
            
            # Map type names to QVariant types
            type_map = {
                'String': QVariant.String,
                'Integer': QVariant.Int,
                'Double': QVariant.Double,
                'Date': QVariant.Date,
                'DateTime': QVariant.DateTime,
                'Boolean': QVariant.Bool
            }
            
            qvar_type = type_map.get(field_type, QVariant.String)
            
            # Create field
            if qvar_type == QVariant.String:
                field = QgsField(field_name, qvar_type, 'text', field_length)
            else:
                field = QgsField(field_name, qvar_type)
                
            fields.append(field)
            
        # Add fields to layer
        provider.addAttributes(fields)
        layer.updateFields()
        
    def validate_layer_compatibility(self, layer: QgsVectorLayer, 
                                   geom_type: str) -> bool:
        """Check if layer is compatible with geometry type
        
        Args:
            layer: Layer to check
            geom_type: Desired geometry type
            
        Returns:
            True if compatible
        """
        if not layer or not layer.isValid():
            return False
            
        # Get layer geometry type
        layer_wkb_type = layer.wkbType()
        layer_geom_type = QgsWkbTypes.geometryType(layer_wkb_type)
        
        # Map string geometry types to QGIS geometry types
        geom_type_map = {
            "Point": QgsWkbTypes.PointGeometry,
            "LineString": QgsWkbTypes.LineGeometry,
            "Polygon": QgsWkbTypes.PolygonGeometry
        }
        
        desired_geom_type = geom_type_map.get(geom_type)
        
        return layer_geom_type == desired_geom_type
        
    def get_layer_fields_info(self, layer: QgsVectorLayer) -> List[Dict[str, any]]:
        """Get information about layer fields
        
        Args:
            layer: Vector layer
            
        Returns:
            List of field information dictionaries
        """
        fields_info = []
        
        for field in layer.fields():
            field_info = {
                'name': field.name(),
                'type': field.typeName(),
                'length': field.length(),
                'precision': field.precision(),
                'comment': field.comment()
            }
            fields_info.append(field_info)
            
        return fields_info