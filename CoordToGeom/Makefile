# Makefile for CoordToGeom plugin

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
