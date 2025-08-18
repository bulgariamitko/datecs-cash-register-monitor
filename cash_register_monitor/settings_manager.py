import json
import os
from typing import Dict, Any


class SettingsManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.default_settings = {
            "ip_address": "192.168.1.155",
            "port": 4999,  # Standard Datecs communication port
            "check_interval": 5,
            "auto_start": True,
            "minimize_to_tray": True
        }
        self.settings = self.load_settings()
    
    def get_config_path(self) -> str:
        """Get the full path to the config file"""
        app_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(app_dir, self.config_file)
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from JSON file, create with defaults if not exists"""
        config_path = self.get_config_path()
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    loaded_settings = json.load(f)
                
                # Merge with defaults to ensure all keys exist
                settings = self.default_settings.copy()
                settings.update(loaded_settings)
                return settings
            else:
                # Create config file with defaults
                self.save_settings(self.default_settings)
                return self.default_settings.copy()
                
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading settings: {e}")
            return self.default_settings.copy()
    
    def save_settings(self, settings: Dict[str, Any] = None) -> bool:
        """Save settings to JSON file"""
        if settings is None:
            settings = self.settings
        
        config_path = self.get_config_path()
        
        try:
            with open(config_path, 'w') as f:
                json.dump(settings, f, indent=4)
            self.settings = settings
            return True
        except IOError as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_setting(self, key: str, default=None):
        """Get a specific setting value"""
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value: Any):
        """Set a specific setting value"""
        self.settings[key] = value
    
    def update_settings(self, **kwargs):
        """Update multiple settings at once"""
        self.settings.update(kwargs)
    
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self.settings = self.default_settings.copy()
        return self.save_settings()
    
    def validate_settings(self) -> Dict[str, str]:
        """Validate current settings and return any errors"""
        errors = {}
        
        # Validate IP address
        ip = self.settings.get("ip_address", "")
        if not ip:
            errors["ip_address"] = "IP address cannot be empty"
        else:
            parts = ip.split(".")
            if len(parts) != 4:
                errors["ip_address"] = "Invalid IP address format"
            else:
                try:
                    for part in parts:
                        num = int(part)
                        if not 0 <= num <= 255:
                            errors["ip_address"] = "Invalid IP address range"
                            break
                except ValueError:
                    errors["ip_address"] = "Invalid IP address format"
        
        # Validate port
        port = self.settings.get("port", 0)
        try:
            port_num = int(port)
            if not 1 <= port_num <= 65535:
                errors["port"] = "Port must be between 1 and 65535"
        except (ValueError, TypeError):
            errors["port"] = "Port must be a valid number"
        
        # Validate check interval
        interval = self.settings.get("check_interval", 0)
        try:
            interval_num = int(interval)
            if interval_num < 1:
                errors["check_interval"] = "Check interval must be at least 1 second"
        except (ValueError, TypeError):
            errors["check_interval"] = "Check interval must be a valid number"
        
        return errors
    
    def get_connection_settings(self) -> Dict[str, Any]:
        """Get settings specifically for connection monitoring"""
        return {
            "ip": self.settings.get("ip_address", "192.168.1.155"),
            "port": self.settings.get("port", 4999),
            "interval": self.settings.get("check_interval", 5)
        }