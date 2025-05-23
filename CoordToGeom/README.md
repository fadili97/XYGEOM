# CoordToGeom Enhanced - QGIS Plugin

A QGIS plugin for creating geometries from coordinates with enhanced features and improved user experience.

## Features

### 🎯 Core Features
- **Multiple Input Methods**: Manual input or file import (TXT/CSV)
- **Flexible Coordinate Formats**: 
  - Space-separated: `100 200`
  - Comma-separated: `100,200`
  - Tab-separated: `100    200`
  - With IDs: `P1 100 200` or `P1,100,200`
- **Geometry Types**: Point, LineString, Polygon
- **Layer Management**: Create new layers or add to existing ones
- **Custom Attributes**: Define and manage attribute table structure

### 🚀 Enhanced Features
- **Tabbed Interface**: Organized UI with Input, Attributes, and Settings tabs
- **File Import**: Batch import coordinates from text files
- **Preview Function**: Preview geometry before creation
- **Auto-detection**: Automatically detect coordinate format
- **Error Handling**: Comprehensive error messages and logging
- **Flexible CRS**: Use project CRS or select custom CRS

## Installation

1. Copy the entire plugin folder to your QGIS plugins directory:
   - Windows: `C:\Users\[Username]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`

2. Restart QGIS

3. Enable the plugin in QGIS:
   - Go to `Plugins` → `Manage and Install Plugins`
   - Search for "CoordToGeom Enhanced"
   - Check the box to enable it

## Usage

### Quick Start

1. Click the CoordToGeom icon in the toolbar or go to `Vector` → `Coordinates to Geometry`

2. **Manual Input**:
   - Select "Manual Input" radio button
   - Enter coordinates in the text area (one pair per line)
   - Choose geometry type (Point, LineString, or Polygon)
   - Enter a layer name
   - Click "Create Geometry"

3. **File Import**:
   - Select "Import from File" radio button
   - Click "Browse..." to select your coordinate file
   - The plugin will auto-detect the format
   - Configure settings as needed
   - Click "Create Geometry"

### Coordinate Formats

#### Without IDs
```
100.5 200.3
150.7 250.8
200.2 300.1
```

#### With IDs (space-separated)
```
P1 100.5 200.3
P2 150.7 250.8
P3 200.2 300.1
```

#### With IDs (comma-separated)
```
P1,100.5,200.3
P2,150.7,250.8
P3,200.2,300.1
```

### Advanced Features

#### Custom Attributes
1. Go to the "Attributes" tab
2. Click "Add Field" to add custom fields
3. Set field name, type, and default value
4. Fields will be added to the created layer

#### Adding to Existing Layers
1. In the "Settings" tab, select "Add to existing layer"
2. Choose the target layer from the dropdown
3. The plugin will validate geometry compatibility
4. Click "Load from Layer" in Attributes tab to match existing structure

#### Polygon Creation
- For polygons, the plugin can auto-close the shape
- Enable "Auto-close polygons" in Settings
- Minimum 3 points required

## File Structure

```
CoordToGeom/
├── __init__.py              # Plugin initialization
├── coord_to_geom.py         # Main plugin class
├── metadata.txt             # Plugin metadata
├── icons/
│   └── icon.png            # Plugin icon
├── gui/
│   └── main_dialog.py      # Main dialog UI
├── core/
│   ├── coordinate_parser.py # Coordinate parsing logic
│   ├── geometry_creator.py  # Geometry creation logic
│   ├── layer_manager.py     # Layer management
│   ├── file_importer.py     # File import handling
│   ├── attribute_manager.py # Attribute management
│   └── logger.py           # Logging utility
└── test/
    └── sample_coordinates.txt # Sample test file
```

## Debugging

The plugin includes comprehensive logging for debugging:

1. **QGIS Message Log**: Check `View` → `Panels` → `Log Messages`
2. **Log Files**: Located in `~/.qgis_coord_to_geom_logs/`
3. **Debug Mode**: Detailed logging of all operations

## Error Messages

Common errors and solutions:

- **"No valid coordinates found"**: Check coordinate format
- **"Please enter a layer name"**: Layer name is required for new layers
- **"Need at least X points"**: Ensure minimum points for geometry type
- **"Invalid coordinate format"**: Use supported formats (see above)

## Requirements

- QGIS 3.0 or higher
- Python 3.6+

## License

This plugin is released under the GNU General Public License v2.0.

## Support

- Report issues: [GitHub Issues](http://github.com/yourusername/CoordToGeom/issues)
- Documentation: [GitHub Wiki](http://github.com/yourusername/CoordToGeom/wiki)
- Email: contact@elfadilygeoconseil.com

## Contributing

Contributions are welcome! Please submit pull requests or open issues on GitHub.

## Changelog

### Version 2.0 (Current)
- Complete UI/UX redesign with tabbed interface
- Added file import functionality
- Support for multiple coordinate formats
- Ability to add geometries to existing layers
- Custom attribute table management
- Enhanced error handling and logging
- Preview functionality

### Version 1.0
- Initial release
- Basic coordinate input
- Simple geometry creation