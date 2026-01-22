# Datecs Cash Register Monitor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos)

A cross-platform application that continuously monitors the connection to Datecs cash registers and provides real-time visual feedback through system tray/menu bar icons.

Perfect for retail environments using Datecs fiscal printers and cash registers to ensure continuous connectivity monitoring.

## 📁 Project Structure

```
datecs-cash-register-monitor/
├── mac/                    # macOS application
│   ├── unified_monitor.py  # Menu bar app using rumps
│   ├── FPrintMonitor.spec  # PyInstaller spec for macOS
│   └── requirements.txt    # macOS dependencies
├── win/                    # Windows application
│   ├── cash_register_monitor/  # Main application package
│   ├── build_executable.py     # Build script
│   ├── build_windows_exe.bat   # One-click build
│   ├── install_and_run.bat     # Quick install & run
│   └── ...                     # Other Windows files
├── README.md
├── LICENSE
└── requirements.txt        # Shared requirements
```

---

## 🍎 macOS Installation

### Requirements
- macOS 10.14+
- Python 3.8+
- Wine (for running FPrint.exe)

### Quick Start

1. **Install dependencies**:
   ```bash
   cd mac
   pip3 install -r requirements.txt
   brew install wine-stable  # If running FPrint.exe
   ```

2. **Run the monitor**:
   ```bash
   python3 unified_monitor.py
   ```

3. **Configure** via menu bar icon → Settings:
   - Set your printer IP and port

### macOS Features

- 🖨️ **Printer icon**: Both FPrint and printer connected
- 🟡 **Yellow icon**: One system running (partial connection)
- 🔴 **Red icon**: Both systems down

### Menu Options
- **Start FPrint**: Launch FPrint.exe via Wine
- **Restart FPrint**: Kill and restart FPrint
- **Settings**: Configure printer IP:port
- **Quit All**: Stop FPrint and exit monitor

---

## 🪟 Windows Installation

### Quick Start (Easiest)

1. [Download the latest release](https://github.com/bulgariamitko/datecs-cash-register-monitor/releases)
2. Extract the ZIP file
3. Navigate to the `win/` folder
4. **Double-click `install_and_run.bat`**
5. The app will install dependencies and start in your system tray!

### Build Executable

1. Navigate to `win/` folder
2. **Double-click `build_windows_exe.bat`** to create `DatecsCashRegisterMonitor.exe`
3. Run the `.exe` file - no Python installation needed!

### Windows Features

- 🟢 **Green icon**: Connected to cash register
- 🔴 **Red icon**: Disconnected from cash register
- 🟡 **Yellow icon**: Checking connection status

### Windows Batch Files

| File | Purpose |
|------|---------|
| `install_and_run.bat` | One-click install & start |
| `build_windows_exe.bat` | Create standalone executable |
| `run_datecs_monitor.bat` | Smart launcher |
| `start_silent.bat` | Silent background startup |

---

## 🏪 Datecs Compatibility

This application is designed for Datecs cash registers and fiscal printers:

- **Datecs FP-2000** series
- **Datecs FP-700** series
- **Datecs WP-500** series
- **Datecs DP-25** and DP-35 series
- Other Datecs devices with network connectivity

**Default Configuration:**
- Port: 4999 (standard Datecs communication port)
- Connection Type: TCP Socket

---

## ⚙️ Configuration

### macOS
Configuration stored at: `~/.config/fprint_monitor/config.json`

```json
{
  "printer_ip": "192.168.1.155",
  "printer_port": 4999
}
```

### Windows
Configuration stored in: `win/config.json`

```json
{
  "ip_address": "192.168.1.155",
  "port": 4999,
  "check_interval": 5,
  "auto_start": true,
  "minimize_to_tray": true
}
```

---

## 🔧 Troubleshooting

### Cannot connect to cash register
1. Verify IP address and port in settings
2. Ensure cash register is powered on and network-enabled
3. Check network connectivity: `ping <IP_ADDRESS>`
4. Test port: `nc -zv <IP_ADDRESS> <PORT>`

### macOS: FPrint not starting
1. Ensure Wine is installed: `brew install wine-stable`
2. Check FPrint.exe exists in parent directory
3. Run from terminal to see debug output

### Windows: Tray icon not visible
1. Check Windows notification area settings
2. Enable "Show all icons in the notification area"
3. Restart the application

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Version History

### v1.2.0 - Cross-Platform Support
- Added macOS menu bar application
- Restructured project with `mac/` and `win/` folders
- FPrint.exe support via Wine on macOS
- Improved restart functionality

### v1.1.0 - Easy Windows Installation
- One-Click Installation with `install_and_run.bat`
- Executable Builder for standalone .exe
- Background execution without command windows

### v1.0.0 - Initial Release
- TCP connection monitoring for Datecs devices
- Windows system tray integration
- Settings management GUI
