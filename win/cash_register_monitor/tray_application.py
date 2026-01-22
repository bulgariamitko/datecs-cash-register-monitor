import pystray
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw
import threading
import os
import sys
from datetime import datetime
try:
    from .connection_monitor import ConnectionMonitor
    from .settings_manager import SettingsManager
except ImportError:
    from connection_monitor import ConnectionMonitor
    from settings_manager import SettingsManager


class SettingsWindow:
    def __init__(self, parent, settings_manager: SettingsManager, on_save_callback=None):
        self.parent = parent
        self.settings_manager = settings_manager
        self.on_save_callback = on_save_callback
        self.window = None
        
    def show(self):
        if self.window is not None:
            self.window.lift()
            self.window.focus_set()
            return
            
        self.window = tk.Toplevel()
        self.window.title("Cash Register Monitor - Settings")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # Center the window
        self.window.transient(self.parent)
        self.window.grab_set()
        
        self.create_widgets()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # IP Address
        ttk.Label(main_frame, text="Cash Register IP Address:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.ip_var = tk.StringVar(value=self.settings_manager.get_setting("ip_address"))
        ip_entry = ttk.Entry(main_frame, textvariable=self.ip_var, width=20)
        ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Port
        ttk.Label(main_frame, text="Port:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.port_var = tk.StringVar(value=str(self.settings_manager.get_setting("port")))
        port_entry = ttk.Entry(main_frame, textvariable=self.port_var, width=20)
        port_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Check Interval
        ttk.Label(main_frame, text="Check Interval (seconds):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.interval_var = tk.StringVar(value=str(self.settings_manager.get_setting("check_interval")))
        interval_entry = ttk.Entry(main_frame, textvariable=self.interval_var, width=20)
        interval_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Auto Start
        self.auto_start_var = tk.BooleanVar(value=self.settings_manager.get_setting("auto_start"))
        auto_start_check = ttk.Checkbutton(main_frame, text="Start with Windows", variable=self.auto_start_var)
        auto_start_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        # Minimize to Tray
        self.minimize_var = tk.BooleanVar(value=self.settings_manager.get_setting("minimize_to_tray"))
        minimize_check = ttk.Checkbutton(main_frame, text="Minimize to system tray", variable=self.minimize_var)
        minimize_check.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Save", command=self.save_settings).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.on_close).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Test Connection", command=self.test_connection).pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
    def test_connection(self):
        try:
            ip = self.ip_var.get().strip()
            port = int(self.port_var.get().strip())
            
            # Create temporary monitor for testing
            test_monitor = ConnectionMonitor(ip, port, 5)
            connected = test_monitor.test_connection()
            
            if connected:
                messagebox.showinfo("Connection Test", f"Successfully connected to {ip}:{port}")
            else:
                messagebox.showwarning("Connection Test", f"Failed to connect to {ip}:{port}")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid port number")
        except Exception as e:
            messagebox.showerror("Error", f"Connection test failed: {str(e)}")
    
    def save_settings(self):
        try:
            # Validate inputs
            ip = self.ip_var.get().strip()
            port = int(self.port_var.get().strip())
            interval = int(self.interval_var.get().strip())
            
            if not ip:
                raise ValueError("IP address cannot be empty")
            if not 1 <= port <= 65535:
                raise ValueError("Port must be between 1 and 65535")
            if interval < 1:
                raise ValueError("Check interval must be at least 1 second")
            
            # Update settings
            self.settings_manager.update_settings(
                ip_address=ip,
                port=port,
                check_interval=interval,
                auto_start=self.auto_start_var.get(),
                minimize_to_tray=self.minimize_var.get()
            )
            
            # Save to file
            if self.settings_manager.save_settings():
                messagebox.showinfo("Settings", "Settings saved successfully!")
                if self.on_save_callback:
                    self.on_save_callback()
                self.on_close()
            else:
                messagebox.showerror("Error", "Failed to save settings")
                
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def on_close(self):
        if self.window:
            self.window.destroy()
            self.window = None


class TrayApplication:
    def __init__(self):
        self.settings_manager = SettingsManager()
        self.monitor = None
        self.icon = None
        self.settings_window = None
        
        # Initialize monitor with current settings
        self.restart_monitor()
        
    def create_icon_image(self, color: str) -> Image.Image:
        """Create a colored circle icon"""
        width = height = 64
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Color mapping
        colors = {
            'green': (0, 255, 0, 255),
            'red': (255, 0, 0, 255),
            'yellow': (255, 255, 0, 255),
            'gray': (128, 128, 128, 255)
        }
        
        color_rgba = colors.get(color, colors['gray'])
        
        # Draw circle
        margin = 8
        draw.ellipse([margin, margin, width-margin, height-margin], fill=color_rgba)
        
        return image
    
    def get_tooltip_text(self) -> str:
        """Generate tooltip text based on current status"""
        if self.monitor:
            status = self.monitor.get_status()
            connected_text = "Connected" if status['connected'] else "Disconnected"
            target = status['target']
            
            if status['last_check']:
                time_str = status['last_check'].strftime("%H:%M:%S")
                return f"Cash Register: {connected_text}\nTarget: {target}\nLast check: {time_str}"
            else:
                return f"Cash Register: {connected_text}\nTarget: {target}"
        return "Cash Register Monitor"
    
    def on_connection_change(self, connected: bool, timestamp: datetime):
        """Callback when connection status changes"""
        if self.icon:
            color = 'green' if connected else 'red'
            self.icon.icon = self.create_icon_image(color)
            self.icon.title = self.get_tooltip_text()
    
    def restart_monitor(self):
        """Restart monitor with current settings"""
        if self.monitor:
            self.monitor.stop_monitoring()
        
        conn_settings = self.settings_manager.get_connection_settings()
        self.monitor = ConnectionMonitor(**conn_settings)
        self.monitor.set_connection_callback(self.on_connection_change)
        self.monitor.start_monitoring()
    
    def show_settings(self, icon=None, item=None):
        """Show settings window"""
        def show_in_main_thread():
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            
            self.settings_window = SettingsWindow(
                root, 
                self.settings_manager, 
                on_save_callback=self.on_settings_saved
            )
            self.settings_window.show()
            
            root.mainloop()
        
        # Run in separate thread to avoid blocking
        threading.Thread(target=show_in_main_thread, daemon=True).start()
    
    def on_settings_saved(self):
        """Callback when settings are saved"""
        self.restart_monitor()
    
    def show_status(self, icon=None, item=None):
        """Show current status in message box"""
        def show_in_main_thread():
            root = tk.Tk()
            root.withdraw()
            
            if self.monitor:
                status = self.monitor.get_status()
                connected_text = "✅ Connected" if status['connected'] else "❌ Disconnected"
                target = status['target']
                
                if status['last_check']:
                    time_str = status['last_check'].strftime("%Y-%m-%d %H:%M:%S")
                    message = f"Status: {connected_text}\nTarget: {target}\nLast check: {time_str}"
                else:
                    message = f"Status: {connected_text}\nTarget: {target}"
            else:
                message = "Monitor not initialized"
            
            messagebox.showinfo("Cash Register Status", message)
            root.destroy()
        
        threading.Thread(target=show_in_main_thread, daemon=True).start()
    
    def quit_application(self, icon=None, item=None):
        """Quit the application"""
        if self.monitor:
            self.monitor.stop_monitoring()
        if self.icon:
            self.icon.stop()
    
    def create_menu(self):
        """Create system tray context menu"""
        return pystray.Menu(
            pystray.MenuItem("Status", self.show_status),
            pystray.MenuItem("Settings", self.show_settings),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit_application)
        )
    
    def run(self):
        """Start the system tray application"""
        # Initial icon (gray until first check)
        icon_image = self.create_icon_image('gray')
        
        self.icon = pystray.Icon(
            "cash_register_monitor",
            icon_image,
            "Cash Register Monitor",
            menu=self.create_menu()
        )
        
        # Update icon after first connection check
        if self.monitor:
            initial_status = self.monitor.get_status()
            color = 'green' if initial_status['connected'] else 'red'
            self.icon.icon = self.create_icon_image(color)
            self.icon.title = self.get_tooltip_text()
        
        # Run the tray icon
        self.icon.run()