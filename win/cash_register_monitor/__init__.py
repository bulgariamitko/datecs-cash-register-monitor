"""
Datecs Cash Register Monitor

A Windows system tray application that continuously monitors 
Datecs cash register connectivity and provides real-time visual feedback.
"""

__version__ = "1.0.0"
__author__ = "Dimitar Klaturov"

from .connection_monitor import ConnectionMonitor
from .settings_manager import SettingsManager
from .tray_application import TrayApplication

__all__ = [
    "ConnectionMonitor",
    "SettingsManager", 
    "TrayApplication"
]