# -*- coding: utf-8 -*-
"""
Main plugin module for Coordinates to Geometry
"""
import os
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.core import QgsProject, Qgis

from .gui.main_dialog import CoordToGeomDialog
from .core.logger import PluginLogger


class CoordToGeomPlugin(QObject):
    """Main plugin class"""
    
    # Signals
    message_emitted = pyqtSignal(str, Qgis.MessageLevel)
    
    def __init__(self, iface):
        """Constructor
        
        Args:
            iface: QGIS interface instance
        """
        super().__init__()
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.action = None
        self.dialog = None
        
        # Initialize logger
        self.logger = PluginLogger('CoordToGeom')
        
        # Connect signals
        self.message_emitted.connect(self._show_message)
        
    def initGui(self):
        """Create the menu entries and toolbar icons"""
        icon_path = os.path.join(self.plugin_dir, "icons", "icon.png")
        
        # Create action
        self.action = QAction(
            QIcon(icon_path),
            "Coordinates to Geometry",
            self.iface.mainWindow()
        )
        self.action.setObjectName("coordToGeomAction")
        self.action.setWhatsThis("Create geometries from coordinates")
        self.action.setStatusTip("Create geometries from coordinates")
        self.action.triggered.connect(self.run)
        
        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToVectorMenu("&Coordinates to Geometry", self.action)
        
        self.logger.info("Plugin initialized")
        
    def unload(self):
        """Remove the plugin menu item and icon"""
        self.iface.removePluginVectorMenu("&Coordinates to Geometry", self.action)
        self.iface.removeToolBarIcon(self.action)
        
        # Clean up dialog
        if self.dialog:
            self.dialog.close()
            self.dialog = None
            
        self.logger.info("Plugin unloaded")
        
    def run(self):
        """Run method that shows the dialog"""
        try:
            # Create dialog if it doesn't exist
            if not self.dialog:
                self.dialog = CoordToGeomDialog(self.iface, self)
                
            # Show the dialog
            self.dialog.show()
            self.dialog.raise_()
            self.dialog.activateWindow()
            
        except Exception as e:
            self.logger.error(f"Error opening dialog: {str(e)}")
            self.message_emitted.emit(
                f"Error opening dialog: {str(e)}", 
                Qgis.Critical
            )
            
    def _show_message(self, message, level):
        """Show message in QGIS message bar
        
        Args:
            message: Message text
            level: Qgis.MessageLevel
        """
        self.iface.messageBar().pushMessage(
            "Coordinates to Geometry",
            message,
            level=level,
            duration=5 if level == Qgis.Success else 10
        )