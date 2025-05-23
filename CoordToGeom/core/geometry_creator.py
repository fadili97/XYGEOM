# -*- coding: utf-8 -*-
"""
Geometry creator module
Handles creation of geometries and features
"""
from typing import List, Dict
from qgis.core import (QgsFeature, QgsGeometry, QgsPointXY, QgsVectorLayer,
                      QgsField, QgsFields)
from qgis.PyQt.QtCore import QVariant


class GeometryCreator:
    """Create geometries from coordinates"""
    
    def create_features(self, layer: QgsVectorLayer, coordinates: List[Dict[str, any]], 
                       geom_type: str, auto_close_polygon: bool = True) -> int:
        """Create features in the layer
        
        Args:
            layer: Target vector layer
            coordinates: List of coordinate dictionaries
            geom_type: Geometry type to create
            auto_close_polygon: Whether to auto-close polygons
            
        Returns:
            Number of features created
        """
        if not layer or not coordinates:
            return 0
            
        # Start editing
        layer.startEditing()
        
        features_created = 0
        
        try:
            if geom_type == "Point":
                # Create individual point features
                for coord in coordinates:
                    feature = self._create_point_feature(coord, layer.fields())
                    if feature:
                        layer.addFeature(feature)
                        features_created += 1
                        
            elif geom_type == "LineString":
                # Create single line feature from all points
                feature = self._create_line_feature(coordinates, layer.fields())
                if feature:
                    layer.addFeature(feature)
                    features_created = 1
                    
            elif geom_type == "Polygon":
                # Create single polygon feature from all points
                feature = self._create_polygon_feature(
                    coordinates, 
                    layer.fields(), 
                    auto_close_polygon
                )
                if feature:
                    layer.addFeature(feature)
                    features_created = 1
                    
            # Commit changes
            layer.commitChanges()
            
        except Exception as e:
            # Rollback on error
            layer.rollBack()
            raise e
            
        return features_created
        
    def _create_point_feature(self, coord: Dict[str, any], fields: QgsFields) -> QgsFeature:
        """Create a point feature
        
        Args:
            coord: Coordinate dictionary with x, y, and optional attributes
            fields: Layer fields
            
        Returns:
            QgsFeature with point geometry
        """
        feature = QgsFeature(fields)
        
        # Set geometry
        point = QgsPointXY(coord['x'], coord['y'])
        feature.setGeometry(QgsGeometry.fromPointXY(point))
        
        # Set attributes
        self._set_feature_attributes(feature, coord, fields)
        
        return feature
        
    def _create_line_feature(self, coordinates: List[Dict[str, any]], 
                            fields: QgsFields) -> QgsFeature:
        """Create a line feature
        
        Args:
            coordinates: List of coordinate dictionaries
            fields: Layer fields
            
        Returns:
            QgsFeature with line geometry
        """
        feature = QgsFeature(fields)
        
        # Create points
        points = [QgsPointXY(coord['x'], coord['y']) for coord in coordinates]
        
        # Set geometry
        feature.setGeometry(QgsGeometry.fromPolylineXY(points))
        
        # Set attributes (use first coordinate's attributes if available)
        if coordinates:
            self._set_feature_attributes(feature, coordinates[0], fields)
            
        return feature
        
    def _create_polygon_feature(self, coordinates: List[Dict[str, any]], 
                               fields: QgsFields, auto_close: bool) -> QgsFeature:
        """Create a polygon feature
        
        Args:
            coordinates: List of coordinate dictionaries
            fields: Layer fields
            auto_close: Whether to auto-close the polygon
            
        Returns:
            QgsFeature with polygon geometry
        """
        feature = QgsFeature(fields)
        
        # Create points
        points = [QgsPointXY(coord['x'], coord['y']) for coord in coordinates]
        
        # Auto-close polygon if needed
        if auto_close and len(points) >= 3:
            if points[0] != points[-1]:
                points.append(points[0])
                
        # Set geometry
        feature.setGeometry(QgsGeometry.fromPolygonXY([points]))
        
        # Set attributes (use first coordinate's attributes if available)
        if coordinates:
            self._set_feature_attributes(feature, coordinates[0], fields)
            
        return feature
        
    def _set_feature_attributes(self, feature: QgsFeature, coord: Dict[str, any], 
                               fields: QgsFields):
        """Set feature attributes from coordinate data
        
        Args:
            feature: Feature to update
            coord: Coordinate dictionary with potential attributes
            fields: Layer fields
        """
        # Set ID if available and field exists
        if 'id' in coord:
            id_field_idx = fields.lookupField('id')
            if id_field_idx == -1:
                # Try common ID field names
                for field_name in ['ID', 'fid', 'FID', 'name', 'Name']:
                    id_field_idx = fields.lookupField(field_name)
                    if id_field_idx != -1:
                        break
                        
            if id_field_idx != -1:
                feature.setAttribute(id_field_idx, coord['id'])
                
        # Set any additional attributes
        for key, value in coord.items():
            if key not in ['x', 'y', 'id']:
                field_idx = fields.lookupField(key)
                if field_idx != -1:
                    feature.setAttribute(field_idx, value)
                    
    def create_multi_geometry(self, coordinates: List[List[Dict[str, any]]], 
                            geom_type: str) -> QgsGeometry:
        """Create multi-part geometry
        
        Args:
            coordinates: List of coordinate lists for each part
            geom_type: Base geometry type
            
        Returns:
            Multi-part geometry
        """
        if geom_type == "Point":
            # MultiPoint
            points = []
            for coord_list in coordinates:
                points.extend([QgsPointXY(c['x'], c['y']) for c in coord_list])
            return QgsGeometry.fromMultiPointXY(points)
            
        elif geom_type == "LineString":
            # MultiLineString
            lines = []
            for coord_list in coordinates:
                line = [QgsPointXY(c['x'], c['y']) for c in coord_list]
                lines.append(line)
            return QgsGeometry.fromMultiPolylineXY(lines)
            
        elif geom_type == "Polygon":
            # MultiPolygon
            polygons = []
            for coord_list in coordinates:
                ring = [QgsPointXY(c['x'], c['y']) for c in coord_list]
                # Close ring if needed
                if ring[0] != ring[-1]:
                    ring.append(ring[0])
                polygons.append([ring])
            return QgsGeometry.fromMultiPolygonXY(polygons)
            
        return None