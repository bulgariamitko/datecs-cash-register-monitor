# Datecs Cash Register Monitor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)

A Windows system tray application that continuously monitors the connection to Datecs cash registers and provides real-time visual feedback through colored tray icons.

Perfect for retail environments using Datecs fiscal printers and cash registers to ensure continuous connectivity monitoring.

## 🏪 Datecs Compatibility

This application is specifically designed for Datecs cash registers and fiscal printers, including:

- **Datecs FP-2000** series
- **Datecs FP-700** series  
- **Datecs WP-500** series
- **Datecs DP-25** and DP-35 series
- Other Datecs devices with network connectivity

**Default Configuration:**
- Port: 4999 (standard Datecs communication port)
- Connection Type: TCP Socket
- Protocol: Compatible with Datecs network protocol

## Features

### 🔄 Connection Monitoring
- Continuous background monitoring every 5 seconds (configurable)
- TCP socket connection test to specified IP:port
- 3-second timeout handling for reliable testing
- Connection history tracking

### 🎯 System Tray Integration
- Minimizes to Windows 11 system tray (notification area)
- Color-coded status indicators:
  - 🟢 **Green**: Connected to cash register
  - 🔴 **Red**: Disconnected from cash register  
  - 🟡 **Yellow**: Checking connection status
- Tooltip showing connection status and last check time
- Right-click context menu with options

### ⚙️ Settings Management
- **IP Address**: Configure Datecs cash register IP (default: 192.168.1.155)
- **Port**: Configure connection port (default: 4999, standard for Datecs devices)
- **Check Interval**: Adjust monitoring frequency (default: 5 seconds)
- **Auto-start**: Automatically start with Windows 11
- Settings saved to JSON configuration file

### 🚀 Windows Startup Integration
- Auto-start with Windows 11 option
- Registry-based or startup folder integration
- Silent startup with no main window
- Immediate connection monitoring on startup

## Installation

### Option 1: Install from Source

1. **Clone or download** this repository
2. **Install Python 3.8+** if not already installed
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   python cash_register_monitor/main.py
   ```

### Option 2: Build Executable

1. **Install build dependencies**:
   ```bash
   pip install pyinstaller
   ```
2. **Run the build script**:
   ```bash
   python build_executable.py
   ```
3. **Run the executable**:
   ```
   dist/CashRegisterMonitor.exe
   ```

## Usage

### Starting the Application

**From Source:**
```bash
python cash_register_monitor/main.py
```

**From Executable:**
```
CashRegisterMonitor.exe
```

### Command Line Options

```bash
python main.py [options]

Options:
  --setup-startup     Add application to Windows startup
  --remove-startup    Remove application from Windows startup  
  --test-connection   Test connection with current settings
  --help             Show help message
```

### System Tray Usage

1. **Right-click** the tray icon to access the context menu
2. **Status**: View current connection information
3. **Settings**: Configure IP, port, and monitoring options
4. **Quit**: Exit the application

### Settings Configuration

Access settings by right-clicking the tray icon and selecting "Settings":

- **Cash Register IP Address**: The IP address of your Datecs cash register
- **Port**: The port number for connection testing
- **Check Interval**: How often to test the connection (in seconds)
- **Start with Windows**: Enable/disable auto-start functionality
- **Minimize to system tray**: Application behavior setting

## Technical Details

### Architecture

```
cash_register_monitor/
├── main.py                 # Application entry point
├── connection_monitor.py   # TCP connection testing logic
├── settings_manager.py     # JSON configuration management
├── tray_application.py     # System tray interface & GUI
├── startup_manager.py      # Windows startup integration
├── create_icons.py        # Icon generation utility
└── icons/                 # Generated status icons
    ├── connected.ico      # Green (connected)
    ├── disconnected.ico   # Red (disconnected)
    ├── checking.ico       # Yellow (checking)
    └── app_icon.png       # Application icon
```

### Dependencies

- **pystray** (≥0.19.4): System tray integration
- **Pillow** (≥9.0.0): Image processing for icons
- **pywin32** (≥305): Windows-specific functionality (Windows only)

### Connection Testing

The application uses TCP socket connections to test connectivity:

```python
def test_connection(self) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(3)  # 3-second timeout
        result = sock.connect_ex((self.ip, self.port))
        return result == 0  # 0 means successful connection
```

### Threading Model

- **Main Thread**: System tray interface and GUI
- **Monitor Thread**: Background connection testing (daemon thread)
- **Settings Thread**: Non-blocking settings window display

## Configuration

### Default Settings

```json
{
    "ip_address": "192.168.1.155",
    "port": 4999,
    "check_interval": 5,
    "auto_start": true,
    "minimize_to_tray": true
}
```

### Configuration File Location

The configuration file `config.json` is stored in the same directory as the application.

## Troubleshooting

### Common Issues

**Issue**: Application doesn't start
- **Solution**: Check that all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Cannot connect to Datecs cash register
- **Solution**: 
  1. Verify the IP address and port in settings (Datecs devices typically use port 4999)
  2. Use "Test Connection" button in settings
  3. Check network connectivity
  4. Ensure Datecs cash register is powered on and network-enabled
  5. Check if the fiscal printer is in the correct network mode

**Issue**: Tray icon not visible
- **Solution**: 
  1. Check Windows 11 notification area settings
  2. Enable "Show all icons in the notification area"
  3. Restart the application

**Issue**: Auto-start not working
- **Solution**:
  1. Run as administrator when enabling auto-start
  2. Check Windows startup settings
  3. Use command line: `python main.py --setup-startup`

### Debug Mode

Run with verbose output to troubleshoot issues:
```bash
python cash_register_monitor/main.py --test-connection
```

## Development

### Project Structure

The application follows a modular architecture:

- **ConnectionMonitor**: Handles TCP connectivity testing
- **SettingsManager**: Manages JSON configuration files  
- **TrayApplication**: System tray interface and GUI windows
- **StartupManager**: Windows startup integration

### Building from Source

1. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller pytest black flake8
   ```

2. **Run tests** (if available):
   ```bash
   pytest
   ```

3. **Format code**:
   ```bash
   black .
   ```

4. **Build executable**:
   ```bash
   python build_executable.py
   ```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For support and bug reports, please:
- **Issues**: Create an issue in the project repository
- **Discussions**: Use GitHub Discussions for questions and community help

## Version History

### v1.0.0
- Initial release
- TCP connection monitoring
- System tray integration
- Windows startup support
- Settings management with GUI
- Icon-based status indicators