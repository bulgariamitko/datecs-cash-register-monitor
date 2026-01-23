#!/usr/bin/env python3
import rumps
import subprocess
import socket
import time
import json
import os
import shutil

class UnifiedMonitor(rumps.App):
    def __init__(self):
        super(UnifiedMonitor, self).__init__("Monitor", "🖨️")
        self.config_path = os.path.expanduser("~/.config/fprint_monitor/config.json")
        self.load_config()

        self.menu = [
            rumps.MenuItem("FPrint Status: Checking...", callback=None),
            rumps.MenuItem("Printer Status: Checking...", callback=None),
            rumps.separator,
            rumps.MenuItem("Start FPrint", callback=self.start_fprint),
            rumps.MenuItem("Restart FPrint", callback=self.restart_fprint),
            rumps.separator,
            rumps.MenuItem("Settings", callback=self.show_settings),
            rumps.MenuItem("Quit All", callback=self.quit_all)
        ]

        # Start monitoring
        self.timer = rumps.Timer(self.check_status, 5)
        self.timer.start()

        # Initial check
        self.check_status(None)

        # Auto-start FPrint if not running
        if not self.check_fprint_running():
            self.start_fprint(None)

    def load_config(self):
        """Load configuration from file"""
        default_config = {
            "printer_ip": "192.168.1.100",
            "printer_port": 9100
        }

        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_config()
        except:
            self.config = default_config

    def save_config(self):
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass

    def check_fprint_running(self):
        """Check if FPrint.exe is running"""
        result = subprocess.run(
            ["pgrep", "-f", "FPrint.exe"],
            capture_output=True,
            text=True
        )
        print(f"[DEBUG] pgrep FPrint.exe: returncode={result.returncode}, stdout='{result.stdout.strip()}', stderr='{result.stderr.strip()}'")
        return result.returncode == 0

    def check_printer_connection(self):
        """Check if printer is accessible"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((self.config["printer_ip"], self.config["printer_port"]))
            sock.close()
            print(f"[DEBUG] Printer socket connect to {self.config['printer_ip']}:{self.config['printer_port']}: result={result} (0=success)")
            return result == 0
        except Exception as e:
            print(f"[DEBUG] Printer connection error: {e}")
            return False

    def check_status(self, _):
        """Check status of both systems"""
        fprint_running = self.check_fprint_running()
        printer_connected = self.check_printer_connection()

        # Debug logging
        print(f"[DEBUG] FPrint running: {fprint_running}, Printer connected: {printer_connected}")
        print(f"[DEBUG] Printer config: {self.config['printer_ip']}:{self.config['printer_port']}")

        # Update menu items
        fprint_status = "✅ Running" if fprint_running else "❌ Not Running"
        printer_status = "✅ Connected" if printer_connected else "❌ Disconnected"

        self.menu["FPrint Status: Checking..."].title = f"FPrint: {fprint_status}"
        self.menu["Printer Status: Checking..."].title = f"Printer: {printer_status}"

        # Update icon color (use title since we can't use emoji in icon)
        if fprint_running and printer_connected:
            # Both running - GREEN
            self.title = "🖨️"
        elif fprint_running or printer_connected:
            # One running - YELLOW
            self.title = "🟡"
        else:
            # Both down - RED
            self.title = "🔴"

    def show_settings(self, _):
        """Show settings dialog"""
        window = rumps.Window(
            title="Monitor Settings",
            message=f"Enter printer IP address and port:\n\nCurrent: {self.config['printer_ip']}:{self.config['printer_port']}",
            default_text=f"{self.config['printer_ip']}:{self.config['printer_port']}",
            ok="Save",
            cancel="Cancel",
            dimensions=(300, 24)
        )

        response = window.run()
        if response.clicked:
            try:
                parts = response.text.split(":")
                if len(parts) == 2:
                    self.config["printer_ip"] = parts[0].strip()
                    self.config["printer_port"] = int(parts[1].strip())
                    self.save_config()
                    rumps.notification(
                        title="Settings Saved",
                        subtitle="Configuration updated",
                        message=f"Printer: {self.config['printer_ip']}:{self.config['printer_port']}"
                    )
                    # Re-check status immediately
                    self.check_status(None)
                else:
                    rumps.alert("Invalid format. Use: IP:PORT (e.g., 192.168.1.100:9100)")
            except ValueError:
                rumps.alert("Invalid port number. Port must be a number (e.g., 9100)")

    def _launch_fprint(self):
        """Internal method to launch FPrint.exe via wine"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        fprint_dir = os.path.dirname(script_dir)
        fprint_exe = os.path.join(fprint_dir, "FPrint.exe")

        # Check if FPrint.exe exists
        if not os.path.exists(fprint_exe):
            rumps.alert(f"FPrint.exe not found at {fprint_exe}")
            return False

        # Use wine from homebrew directly
        wine_path = "/opt/homebrew/bin/wine"
        if not os.path.exists(wine_path):
            wine_path = "/usr/local/bin/wine"
        if not os.path.exists(wine_path):
            wine_path = shutil.which("wine")

        if not wine_path or not os.path.exists(wine_path):
            rumps.alert("Wine not found. Please install wine via Homebrew: brew install wine-stable")
            return False

        print(f"[DEBUG] Launching FPrint from: {fprint_dir}")
        print(f"[DEBUG] Wine path: {wine_path}")

        # Use nohup + bash -l (login shell) to get full environment
        cmd = f'nohup /bin/bash -l -c \'cd "{fprint_dir}" && "{wine_path}" FPrint.exe\' > /dev/null 2>&1 &'
        print(f"[DEBUG] Running: {cmd}")

        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True

    def start_fprint(self, _):
        """Start FPrint.exe if not running"""
        if not self.check_fprint_running():
            try:
                if self._launch_fprint():
                    # Wait for Wine to initialize
                    time.sleep(4)
                    self.check_status(None)

                    if self.check_fprint_running():
                        rumps.notification(
                            title="FPrint Started",
                            subtitle="",
                            message="FPrint.exe has been started successfully"
                        )
                    else:
                        rumps.alert("FPrint.exe may have failed to start. Please try again.")
            except Exception as e:
                rumps.alert(f"Failed to start FPrint: {str(e)}")
        else:
            rumps.alert("FPrint is already running")

    def restart_fprint(self, _):
        """Restart FPrint.exe"""
        print("[DEBUG] Restarting FPrint...")

        # Kill ALL wine-related processes thoroughly
        subprocess.run(["pkill", "-9", "-f", "FPrint.exe"], stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-9", "-f", "wine"], stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-9", "-f", "wineserver"], stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-9", "-f", "winedevice"], stderr=subprocess.DEVNULL)

        # Wait for processes to fully terminate
        time.sleep(3)

        print("[DEBUG] All wine processes killed, starting FPrint...")

        try:
            if self._launch_fprint():
                # Wait for Wine to initialize
                time.sleep(4)
                self.check_status(None)

                if self.check_fprint_running():
                    rumps.notification(
                        title="FPrint Restarted",
                        subtitle="",
                        message="FPrint.exe has been restarted successfully"
                    )
                else:
                    rumps.alert("FPrint.exe may have failed to restart. Please try again.")
        except Exception as e:
            rumps.alert(f"Failed to restart FPrint: {str(e)}")

    def quit_all(self, _):
        """Quit monitoring and FPrint"""
        # Kill FPrint.exe
        subprocess.run(["pkill", "-f", "FPrint.exe"], stderr=subprocess.DEVNULL)
        # Quit this app
        rumps.quit_application()

if __name__ == "__main__":
    app = UnifiedMonitor()
    app.run()
