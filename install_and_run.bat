@echo off
echo ========================================
echo Datecs Cash Register Monitor Installer
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Python found: 
python --version

:: Navigate to script directory
cd /d "%~dp0"

echo.
echo Installing required dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo Starting Datecs Cash Register Monitor...
echo The application will run in the system tray.
echo You can close this window after the app starts.
echo.

:: Start the application in background
start /B pythonw cash_register_monitor/main.py

echo Application started! Check your system tray for the monitor icon.
echo Right-click the tray icon to access settings.
echo.
timeout /t 5 >nul
echo This window will close automatically...
timeout /t 3 >nul
exit