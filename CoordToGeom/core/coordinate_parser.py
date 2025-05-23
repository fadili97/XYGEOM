# -*- coding: utf-8 -*-
"""
Coordinate parser module
Handles parsing of various coordinate formats
"""
import re
from typing import List, Dict, Optional, Tuple


class CoordinateParser:
    """Parse coordinates from various text formats"""
    
    def __init__(self):
        """Initialize parser with regex patterns"""
        # Patterns for different coordinate formats
        self.patterns = {
            'space': re.compile(r'^(-?\d+\.?\d*)\s+(-?\d+\.?\d*)$'),
            'comma': re.compile(r'^(-?\d+\.?\d*),\s*(-?\d+\.?\d*)$'),
            'tab': re.compile(r'^(-?\d+\.?\d*)\t(-?\d+\.?\d*)$'),
            'id_space': re.compile(r'^(\S+)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)$'),
            'id_comma': re.compile(r'^(\S+),\s*(-?\d+\.?\d*),\s*(-?\d+\.?\d*)$'),
            'id_tab': re.compile(r'^(\S+)\t(-?\d+\.?\d*)\t(-?\d+\.?\d*)$')
        }
        
    def parse_text(self, text: str, separator: Optional[str] = None, 
                   has_id: bool = False) -> List[Dict[str, any]]:
        """Parse coordinate text
        
        Args:
            text: Input text containing coordinates
            separator: Separator to use (None for auto-detect)
            has_id: Whether first column contains IDs
            
        Returns:
            List of coordinate dictionaries with 'x', 'y', and optionally 'id'
        """
        coordinates = []
        lines = text.strip().split('\n')
        
        # Auto-detect separator if not specified
        if separator is None:
            separator = self._detect_separator(lines[0] if lines else "")
            
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                coord = self._parse_line(line, separator, has_id)
                if coord:
                    # Add line number as default ID if no ID provided
                    if 'id' not in coord:
                        coord['id'] = f"P{line_num}"
                    coordinates.append(coord)
            except ValueError as e:
                # Log parsing error but continue with other lines
                print(f"Line {line_num}: {str(e)}")
                continue
                
        return coordinates
        
    def _detect_separator(self, sample_line: str) -> str:
        """Auto-detect the separator used in the text
        
        Args:
            sample_line: A sample line to analyze
            
        Returns:
            Detected separator character
        """
        # Check for common separators
        if ',' in sample_line:
            return ','
        elif '\t' in sample_line:
            return '\t'
        else:
            return ' '  # Default to space
            
    def _parse_line(self, line: str, separator: str, has_id: bool) -> Optional[Dict[str, any]]:
        """Parse a single line of coordinates
        
        Args:
            line: Line to parse
            separator: Separator character
            has_id: Whether line contains ID
            
        Returns:
            Dictionary with parsed coordinates or None
        """
        # Choose pattern based on separator and ID presence
        if has_id:
            if separator == ' ':
                pattern = self.patterns['id_space']
            elif separator == ',':
                pattern = self.patterns['id_comma']
            elif separator == '\t':
                pattern = self.patterns['id_tab']
            else:
                # Fallback to splitting
                parts = line.split(separator)
                if len(parts) >= 3:
                    return {
                        'id': parts[0],
                        'x': float(parts[1]),
                        'y': float(parts[2])
                    }
                raise ValueError(f"Invalid format: expected ID X Y, got '{line}'")
        else:
            if separator == ' ':
                pattern = self.patterns['space']
            elif separator == ',':
                pattern = self.patterns['comma']
            elif separator == '\t':
                pattern = self.patterns['tab']
            else:
                # Fallback to splitting
                parts = line.split(separator)
                if len(parts) >= 2:
                    return {
                        'x': float(parts[0]),
                        'y': float(parts[1])
                    }
                raise ValueError(f"Invalid format: expected X Y, got '{line}'")
                
        # Try pattern matching
        match = pattern.match(line)
        if match:
            if has_id:
                return {
                    'id': match.group(1),
                    'x': float(match.group(2)),
                    'y': float(match.group(3))
                }
            else:
                return {
                    'x': float(match.group(1)),
                    'y': float(match.group(2))
                }
                
        return None
        
    def validate_coordinates(self, coordinates: List[Dict[str, any]], 
                           geom_type: str) -> Tuple[bool, str]:
        """Validate coordinates for geometry type
        
        Args:
            coordinates: List of coordinate dictionaries
            geom_type: Target geometry type
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not coordinates:
            return False, "No coordinates provided"
            
        coord_count = len(coordinates)
        
        if geom_type == "Point":
            if coord_count < 1:
                return False, "Point geometry requires at least 1 coordinate"
        elif geom_type == "LineString":
            if coord_count < 2:
                return False, "LineString geometry requires at least 2 coordinates"
        elif geom_type == "Polygon":
            if coord_count < 3:
                return False, "Polygon geometry requires at least 3 coordinates"
                
        # Check for valid numeric values
        for i, coord in enumerate(coordinates):
            if not isinstance(coord.get('x'), (int, float)) or \
               not isinstance(coord.get('y'), (int, float)):
                return False, f"Invalid numeric values at position {i+1}"
                
        return True, ""