"""
Windows startup integration for Cash Register Monitor
"""

import os
import sys
import shutil


class StartupManager:
    """Manages Windows startup integration"""
    
    def __init__(self):
        self.app_name = "CashRegisterMonitor"
        self.app_description = "Cash Register Connection Monitor"
    
    def get_executable_path(self):
        """Get the path to the current executable or script"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable (PyInstaller)
            return sys.executable
        else:
            # Running as Python script
            main_script = os.path.join(os.path.dirname(__file__), 'main.py')
            return f'"{sys.executable}" "{main_script}"'
    
    def add_to_registry_startup(self):
        """Add application to Windows registry startup (HKEY_CURRENT_USER)"""
        try:
            import winreg
            
            exe_path = self.get_executable_path()
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            # Open the registry key
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                key_path, 
                0, 
                winreg.KEY_SET_VALUE
            )
            
            # Add the application
            winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
            
            return True, "Successfully added to Windows startup (Registry)"
            
        except ImportError:
            return False, "Windows registry access not available on this platform"
        except Exception as e:
            return False, f"Failed to add to registry startup: {str(e)}"
    
    def remove_from_registry_startup(self):
        """Remove application from Windows registry startup"""
        try:
            import winreg
            
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            # Open the registry key
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                key_path, 
                0, 
                winreg.KEY_SET_VALUE
            )
            
            try:
                # Remove the application
                winreg.DeleteValue(key, self.app_name)
                winreg.CloseKey(key)
                return True, "Successfully removed from Windows startup (Registry)"
            except FileNotFoundError:
                winreg.CloseKey(key)
                return True, "Application was not in startup registry"
                
        except ImportError:
            return False, "Windows registry access not available on this platform"
        except Exception as e:
            return False, f"Failed to remove from registry startup: {str(e)}"
    
    def get_startup_folder_path(self):
        """Get Windows startup folder path"""
        try:
            # Get the startup folder path
            startup_folder = os.path.join(
                os.path.expanduser("~"), 
                "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
            )
            
            if os.path.exists(startup_folder):
                return startup_folder
            else:
                # Alternative path
                import winreg
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
                )
                startup_folder = winreg.QueryValueEx(key, "Startup")[0]
                winreg.CloseKey(key)
                return startup_folder
                
        except Exception:
            return None
    
    def add_to_startup_folder(self):
        """Add shortcut to Windows startup folder"""
        try:
            startup_folder = self.get_startup_folder_path()
            if not startup_folder:
                return False, "Could not locate Windows startup folder"
            
            shortcut_path = os.path.join(startup_folder, f"{self.app_name}.lnk")
            
            # Create shortcut using Windows COM
            import win32com.client
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            
            if getattr(sys, 'frozen', False):
                # Executable
                shortcut.Targetpath = sys.executable
                shortcut.WorkingDirectory = os.path.dirname(sys.executable)
            else:
                # Python script
                shortcut.Targetpath = sys.executable
                main_script = os.path.join(os.path.dirname(__file__), 'main.py')
                shortcut.Arguments = f'"{main_script}"'
                shortcut.WorkingDirectory = os.path.dirname(__file__)
            
            shortcut.Description = self.app_description
            shortcut.IconLocation = self.get_icon_path()
            shortcut.save()
            
            return True, f"Successfully added shortcut to startup folder: {shortcut_path}"
            
        except ImportError:
            return False, "win32com not available. Install pywin32: pip install pywin32"
        except Exception as e:
            return False, f"Failed to create startup shortcut: {str(e)}"
    
    def remove_from_startup_folder(self):
        """Remove shortcut from Windows startup folder"""
        try:
            startup_folder = self.get_startup_folder_path()
            if not startup_folder:
                return False, "Could not locate Windows startup folder"
            
            shortcut_path = os.path.join(startup_folder, f"{self.app_name}.lnk")
            
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
                return True, f"Successfully removed startup shortcut: {shortcut_path}"
            else:
                return True, "Startup shortcut was not found"
                
        except Exception as e:
            return False, f"Failed to remove startup shortcut: {str(e)}"
    
    def get_icon_path(self):
        """Get path to application icon"""
        icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'connected.ico')
        if os.path.exists(icon_path):
            return icon_path
        return ""
    
    def is_in_startup_registry(self):
        """Check if application is in registry startup"""
        try:
            import winreg
            
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            
            try:
                value, _ = winreg.QueryValueEx(key, self.app_name)
                winreg.CloseKey(key)
                return True, value
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False, None
                
        except Exception:
            return False, None
    
    def is_in_startup_folder(self):
        """Check if application shortcut is in startup folder"""
        try:
            startup_folder = self.get_startup_folder_path()
            if startup_folder:
                shortcut_path = os.path.join(startup_folder, f"{self.app_name}.lnk")
                return os.path.exists(shortcut_path), shortcut_path
            return False, None
        except Exception:
            return False, None
    
    def add_to_startup(self, method="registry"):
        """Add application to Windows startup using specified method"""
        if method == "registry":
            return self.add_to_registry_startup()
        elif method == "folder":
            return self.add_to_startup_folder()
        else:
            return False, f"Unknown startup method: {method}"
    
    def remove_from_startup(self, method="both"):
        """Remove application from Windows startup"""
        results = []
        
        if method in ["registry", "both"]:
            success, message = self.remove_from_registry_startup()
            results.append(("registry", success, message))
        
        if method in ["folder", "both"]:
            success, message = self.remove_from_startup_folder()
            results.append(("folder", success, message))
        
        return results
    
    def get_startup_status(self):
        """Get current startup status"""
        registry_status, registry_path = self.is_in_startup_registry()
        folder_status, folder_path = self.is_in_startup_folder()
        
        return {
            "registry": {"enabled": registry_status, "path": registry_path},
            "folder": {"enabled": folder_status, "path": folder_path}
        }