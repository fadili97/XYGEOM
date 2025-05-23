# -*- coding: utf-8 -*-
"""
File importer module
Handles importing coordinates from text files
"""
import os
from typing import List, Dict, Optional
from .coordinate_parser import CoordinateParser


class FileImporter:
    """Import coordinates from files"""
    
    def __init__(self):
        """Initialize file importer"""
        self.parser = CoordinateParser()
        
    def import_file(self, file_path: str, encoding: str = 'utf-8') -> List[Dict[str, any]]:
        """Import coordinates from file
        
        Args:
            file_path: Path to file
            encoding: File encoding
            
        Returns:
            List of coordinate dictionaries
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        coordinates = []
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                
            # Detect format and parse
            file_format = self._detect_file_format(content)
            
            if file_format:
                coordinates = self.parser.parse_text(
                    content,
                    separator=file_format['separator'],
                    has_id=file_format['has_id']
                )
                
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                    
                file_format = self._detect_file_format(content)
                if file_format:
                    coordinates = self.parser.parse_text(
                        content,
                        separator=file_format['separator'],
                        has_id=file_format['has_id']
                    )
            except Exception as e:
                raise Exception(f"Error reading file: {str(e)}")
                
        return coordinates
        
    def _detect_file_format(self, content: str) -> Optional[Dict[str, any]]:
        """Detect file format from content
        
        Args:
            content: File content
            
        Returns:
            Format information dictionary
        """
        lines = content.strip().split('\n')
        if not lines:
            return None
            
        # Get sample lines (skip empty lines)
        sample_lines = []
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and not line.startswith('#'):  # Skip comments
                sample_lines.append(line)
                
        if not sample_lines:
            return None
            
        # Analyze first line
        first_line = sample_lines[0]
        
        # Count fields and detect separator
        separators = [',', '\t', ' ', ';']
        detected_format = None
        
        for sep in separators:
            parts = first_line.split(sep)
            clean_parts = [p.strip() for p in parts if p.strip()]
            
            if len(clean_parts) >= 2:
                # Check if parts are numeric (coordinates)
                try:
                    # Try parsing as coordinates
                    float(clean_parts[-2])  # Second to last should be X
                    float(clean_parts[-1])   # Last should be Y
                    
                    # If more than 2 fields, first might be ID
                    has_id = len(clean_parts) > 2
                    
                    detected_format = {
                        'separator': sep,
                        'has_id': has_id,
                        'field_count': len(clean_parts)
                    }
                    break
                    
                except ValueError:
                    continue
                    
        return detected_format
        
    def validate_file(self, file_path: str) -> tuple:
        """Validate file before import
        
        Args:
            file_path: Path to file
            
        Returns:
            Tuple of (is_valid, message)
        """
        # Check file exists
        if not os.path.exists(file_path):
            return False, "File does not exist"
            
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return False, "File is empty"
        elif file_size > 50 * 1024 * 1024:  # 50MB limit
            return False, "File is too large (>50MB)"
            
        # Check file extension
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in ['.txt', '.csv', '.dat', '.xyz']:
            return False, f"Unsupported file type: {ext}"
            
        return True, "File is valid"
        
    def get_file_preview(self, file_path: str, max_lines: int = 10) -> str:
        """Get preview of file contents
        
        Args:
            file_path: Path to file
            max_lines: Maximum lines to preview
            
        Returns:
            Preview string
        """
        preview_lines = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i >= max_lines:
                        break
                    preview_lines.append(line.rstrip())
                    
            if i >= max_lines:
                preview_lines.append("...")
                
        except Exception as e:
            return f"Error reading file: {str(e)}"
            
        return '\n'.join(preview_lines)