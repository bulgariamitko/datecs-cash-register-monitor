"""
Datecs Cash Register Monitor
A Windows system tray application that monitors Datecs cash register connectivity
"""

import sys
import os
import argparse
import tkinter as tk
from tkinter import messagebox

# Add the package directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from .tray_application import TrayApplication
    from .settings_manager import SettingsManager
except ImportError:
    from tray_application import TrayApplication
    from settings_manager import SettingsManager


def setup_windows_startup():
    """Add application to Windows startup (Windows only)"""
    if sys.platform != "win32":
        print("Startup integration is only available on Windows")
        return False
    
    try:
        import winreg
        
        # Get current executable path
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            exe_path = sys.executable
        else:
            # Running as Python script
            exe_path = f'"{sys.executable}" "{os.path.abspath(__file__)}"'
        
        # Registry key for startup programs
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        
        # Add entry
        winreg.SetValueEx(key, "CashRegisterMonitor", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        
        print("Successfully added to Windows startup")
        return True
        
    except Exception as e:
        print(f"Failed to add to startup: {e}")
        return False


def remove_windows_startup():
    """Remove application from Windows startup"""
    if sys.platform != "win32":
        print("Startup integration is only available on Windows")
        return False
    
    try:
        import winreg
        
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        
        try:
            winreg.DeleteValue(key, "CashRegisterMonitor")
            print("Successfully removed from Windows startup")
            return True
        except FileNotFoundError:
            print("Application was not in startup list")
            return True
        finally:
            winreg.CloseKey(key)
            
    except Exception as e:
        print(f"Failed to remove from startup: {e}")
        return False


def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    try:
        import pystray
    except ImportError:
        missing_deps.append("pystray")
    
    try:
        import PIL
    except ImportError:
        missing_deps.append("Pillow")
    
    if missing_deps:
        error_msg = f"Missing required dependencies: {', '.join(missing_deps)}\n"
        error_msg += "Please install them using: pip install " + " ".join(missing_deps)
        
        # Try to show GUI error if tkinter is available
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Missing Dependencies", error_msg)
            root.destroy()
        except:
            print(error_msg)
        
        return False
    
    return True


def show_help():
    """Show help information"""
    help_text = """
Cash Register Connection Monitor

Usage:
    python main.py [options]

Options:
    --setup-startup     Add application to Windows startup
    --remove-startup    Remove application from Windows startup
    --test-connection   Test connection with current settings
    --help             Show this help message

Description:
    This application monitors the connection to a cash register and displays
    the status in the Windows system tray. The tray icon changes color based
    on the connection status:
    
    Green: Connected
    Red: Disconnected
    Yellow: Checking connection
    
    Right-click the tray icon to access settings and other options.
"""
    print(help_text)


def test_connection():
    """Test connection with current settings"""
    try:
        from .connection_monitor import ConnectionMonitor
    except ImportError:
        from connection_monitor import ConnectionMonitor
    
    settings_manager = SettingsManager()
    conn_settings = settings_manager.get_connection_settings()
    
    print(f"Testing connection to {conn_settings['ip']}:{conn_settings['port']}...")
    
    monitor = ConnectionMonitor(**conn_settings)
    connected = monitor.test_connection()
    
    if connected:
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed!")
    
    return connected


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="Cash Register Connection Monitor")
    parser.add_argument("--setup-startup", action="store_true", help="Add to Windows startup")
    parser.add_argument("--remove-startup", action="store_true", help="Remove from Windows startup")
    parser.add_argument("--test-connection", action="store_true", help="Test connection")
    parser.add_argument("--help-extended", action="store_true", help="Show extended help")
    
    args = parser.parse_args()
    
    if args.help_extended:
        show_help()
        return
    
    if args.setup_startup:
        setup_windows_startup()
        return
    
    if args.remove_startup:
        remove_windows_startup()
        return
    
    if args.test_connection:
        test_connection()
        return
    
    # Check dependencies before starting
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # Create and run the tray application
        app = TrayApplication()
        
        # Check if auto-startup should be configured
        settings_manager = SettingsManager()
        if settings_manager.get_setting("auto_start") and sys.platform == "win32":
            setup_windows_startup()
        
        print("Starting Cash Register Monitor...")
        print("Application will run in system tray. Right-click the tray icon for options.")
        
        # Run the application
        app.run()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        error_msg = f"Application error: {str(e)}"
        print(error_msg)
        
        # Try to show GUI error
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Application Error", error_msg)
            root.destroy()
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()