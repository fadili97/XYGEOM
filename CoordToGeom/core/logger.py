# -*- coding: utf-8 -*-
"""
Logger module
Handles plugin logging for debugging
"""
import os
import logging
from datetime import datetime
from qgis.core import QgsMessageLog, Qgis


class PluginLogger:
    """Custom logger for plugin debugging"""
    
    def __init__(self, name: str, log_to_file: bool = True):
        """Initialize logger
        
        Args:
            name: Logger name
            log_to_file: Whether to log to file
        """
        self.name = name
        self.log_to_file = log_to_file
        
        # Setup Python logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Setup file logging if enabled
        if log_to_file:
            self._setup_file_logging()
            
    def _setup_file_logging(self):
        """Setup file logging"""
        # Create log directory
        log_dir = os.path.join(os.path.expanduser('~'), '.qgis_coord_to_geom_logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(log_dir, f'{self.name}_{timestamp}.log')
        
        # Create file handler
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(file_handler)
        
    def debug(self, message: str):
        """Log debug message
        
        Args:
            message: Message to log
        """
        self.logger.debug(message)
        QgsMessageLog.logMessage(message, self.name, Qgis.Info)
        
    def info(self, message: str):
        """Log info message
        
        Args:
            message: Message to log
        """
        self.logger.info(message)
        QgsMessageLog.logMessage(message, self.name, Qgis.Info)
        
    def warning(self, message: str):
        """Log warning message
        
        Args:
            message: Message to log
        """
        self.logger.warning(message)
        QgsMessageLog.logMessage(message, self.name, Qgis.Warning)
        
    def error(self, message: str):
        """Log error message
        
        Args:
            message: Message to log
        """
        self.logger.error(message)
        QgsMessageLog.logMessage(message, self.name, Qgis.Critical)
        
    def critical(self, message: str):
        """Log critical message
        
        Args:
            message: Message to log
        """
        self.logger.critical(message)
        QgsMessageLog.logMessage(message, self.name, Qgis.Critical)
        
    def exception(self, message: str):
        """Log exception with traceback
        
        Args:
            message: Message to log
        """
        self.logger.exception(message)
        QgsMessageLog.logMessage(f"{message}\n{self._get_traceback()}", 
                               self.name, Qgis.Critical)
        
    def _get_traceback(self) -> str:
        """Get current traceback as string
        
        Returns:
            Traceback string
        """
        import traceback
        return traceback.format_exc()
        
    def log_function_call(self, func_name: str, **kwargs):
        """Log function call with parameters
        
        Args:
            func_name: Function name
            **kwargs: Function parameters
        """
        params = ', '.join([f"{k}={v}" for k, v in kwargs.items()])
        self.debug(f"Calling {func_name}({params})")
        
    def log_function_result(self, func_name: str, result: any):
        """Log function result
        
        Args:
            func_name: Function name
            result: Function result
        """
        self.debug(f"{func_name} returned: {result}")