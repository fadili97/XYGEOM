#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to create the enhanced CoordToGeom plugin structure
Run this script in the directory where you want to create the plugin
"""

import os
import sys

def create_plugin_structure():
    """Create all directories and files for the plugin"""
    
    # Define the plugin directory structure
    plugin_name = "CoordToGeom"
    
    # Directory structure
    directories = [
        plugin_name,
        os.path.join(plugin_name, "gui"),
        os.path.join(plugin_name, "core"),
        os.path.join(plugin_name, "icons"),
        os.path.join(plugin_name, "test"),
    ]
    
    # File structure with descriptions
    files = {
        # Root level files
        os.path.join(plugin_name, "__init__.py"): "# Plugin initialization file\n",
        os.path.join(plugin_name, "coord_to_geom.py"): "# Main plugin class\n",
        os.path.join(plugin_name, "metadata.txt"): "# Plugin metadata\n",
        os.path.join(plugin_name, "README.md"): "# Plugin documentation\n",
        os.path.join(plugin_name, ".gitignore"): "# Git ignore file\n",
        
        # GUI files
        os.path.join(plugin_name, "gui", "__init__.py"): "",
        os.path.join(plugin_name, "gui", "main_dialog.py"): "# Main dialog class\n",
        
        # Core module files
        os.path.join(plugin_name, "core", "__init__.py"): "",
        os.path.join(plugin_name, "core", "coordinate_parser.py"): "# Coordinate parsing logic\n",
        os.path.join(plugin_name, "core", "geometry_creator.py"): "# Geometry creation logic\n",
        os.path.join(plugin_name, "core", "layer_manager.py"): "# Layer management logic\n",
        os.path.join(plugin_name, "core", "file_importer.py"): "# File import logic\n",
        os.path.join(plugin_name, "core", "attribute_manager.py"): "# Attribute management logic\n",
        os.path.join(plugin_name, "core", "logger.py"): "# Logging utility\n",
        
        # Test files
        os.path.join(plugin_name, "test", "__init__.py"): "",
        os.path.join(plugin_name, "test", "sample_coordinates.txt"): "# Sample coordinate file\n",
        os.path.join(plugin_name, "test", "test_parser.py"): "# Unit tests for parser\n",
        os.path.join(plugin_name, "test", "test_geometry.py"): "# Unit tests for geometry\n",
        
        # Icon placeholder
        os.path.join(plugin_name, "icons", "icon.png"): "ICON_PLACEHOLDER",
    }
    
    # Additional empty directories that might be needed
    additional_dirs = [
        os.path.join(plugin_name, "resources"),
        os.path.join(plugin_name, "i18n"),  # For translations
    ]
    
    print(f"Creating {plugin_name} plugin structure...")
    print("-" * 50)
    
    # Create directories
    for directory in directories + additional_dirs:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✓ Created directory: {directory}")
        except Exception as e:
            print(f"✗ Error creating directory {directory}: {e}")
    
    print("-" * 50)
    
    # Create files
    for filepath, content in files.items():
        try:
            # Special handling for icon placeholder
            if content == "ICON_PLACEHOLDER":
                # Create a simple placeholder text file for the icon
                with open(filepath, 'w') as f:
                    f.write("Replace this with actual icon.png file")
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            print(f"✓ Created file: {filepath}")
        except Exception as e:
            print(f"✗ Error creating file {filepath}: {e}")
    
    # Create a Makefile
    makefile_path = os.path.join(plugin_name, "Makefile")
    makefile_content = """# Makefile for CoordToGeom plugin

PLUGINNAME = CoordToGeom

# QGIS3 default plugin directory
QGIS3_PLUGIN_DIR := $(HOME)/.local/share/QGIS/QGIS3/profiles/default/python/plugins

help:
	@echo "make deploy - Deploy plugin to QGIS plugin directory"
	@echo "make clean - Remove compiled files"
	@echo "make zip - Create plugin zip file"

deploy:
	@echo "Deploying plugin to $(QGIS3_PLUGIN_DIR)/$(PLUGINNAME)"
	@mkdir -p $(QGIS3_PLUGIN_DIR)/$(PLUGINNAME)
	@cp -r * $(QGIS3_PLUGIN_DIR)/$(PLUGINNAME)/
	@echo "Plugin deployed!"

clean:
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@echo "Cleaned compiled files"

zip:
	@echo "Creating plugin zip file"
	@rm -f $(PLUGINNAME).zip
	@zip -r $(PLUGINNAME).zip . -x "*.pyc" -x "*__pycache__*" -x "*.git*" -x "Makefile"
	@echo "Created $(PLUGINNAME).zip"

.PHONY: help deploy clean zip
"""
    
    try:
        with open(makefile_path, 'w') as f:
            f.write(makefile_content)
        print(f"✓ Created file: {makefile_path}")
    except Exception as e:
        print(f"✗ Error creating Makefile: {e}")
    
    # Create requirements.txt for development
    requirements_path = os.path.join(plugin_name, "requirements-dev.txt")
    requirements_content = """# Development requirements
pytest>=6.0
pytest-qt>=4.0
pytest-cov>=2.0
black>=21.0
flake8>=3.9
pylint>=2.8
"""
    
    try:
        with open(requirements_path, 'w') as f:
            f.write(requirements_content)
        print(f"✓ Created file: {requirements_path}")
    except Exception as e:
        print(f"✗ Error creating requirements file: {e}")
    
    print("-" * 50)
    print(f"\n✓ Plugin structure created successfully in '{plugin_name}' directory!")
    print("\nNext steps:")
    print("1. Copy the code from the artifacts into the respective files")
    print("2. Add a proper icon.png file to the icons directory")
    print("3. Run 'make deploy' to install the plugin to QGIS")
    print("4. Restart QGIS and enable the plugin")
    
    # Create a simple shell script for Linux/Mac users
    if sys.platform != 'win32':
        deploy_script = os.path.join(plugin_name, "deploy.sh")
        deploy_content = """#!/bin/bash
# Deploy script for CoordToGeom plugin

PLUGIN_NAME="CoordToGeom"
QGIS_PLUGINS_DIR="$HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins"

echo "Deploying $PLUGIN_NAME to QGIS..."
mkdir -p "$QGIS_PLUGINS_DIR/$PLUGIN_NAME"
cp -r ./* "$QGIS_PLUGINS_DIR/$PLUGIN_NAME/"
echo "Plugin deployed! Please restart QGIS."
"""
        try:
            with open(deploy_script, 'w') as f:
                f.write(deploy_content)
            os.chmod(deploy_script, 0o755)  # Make executable
            print(f"✓ Created deployment script: {deploy_script}")
        except Exception as e:
            print(f"✗ Error creating deployment script: {e}")

def create_vscode_settings():
    """Create VS Code settings for better development experience"""
    vscode_dir = os.path.join("CoordToGeom", ".vscode")
    os.makedirs(vscode_dir, exist_ok=True)
    
    # VS Code settings
    settings_content = {
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": True,
        "python.formatting.provider": "black",
        "python.linting.flake8Enabled": True,
        "python.linting.flake8Args": ["--max-line-length=100"],
        "files.exclude": {
            "**/__pycache__": True,
            "**/*.pyc": True
        }
    }
    
    launch_content = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Current File",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal"
            }
        ]
    }
    
    import json
    
    try:
        with open(os.path.join(vscode_dir, "settings.json"), 'w') as f:
            json.dump(settings_content, f, indent=4)
        print(f"✓ Created VS Code settings")
        
        with open(os.path.join(vscode_dir, "launch.json"), 'w') as f:
            json.dump(launch_content, f, indent=4)
        print(f"✓ Created VS Code launch configuration")
    except Exception as e:
        print(f"Note: Could not create VS Code settings: {e}")

if __name__ == "__main__":
    # Check if we're in the right place
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    response = input("Create CoordToGeom plugin structure here? (y/n): ")
    
    if response.lower() == 'y':
        create_plugin_structure()
        create_vscode_settings()
    else:
        print("Aborted.")