@echo off
:: Simple launcher for Datecs Cash Register Monitor
:: This file can be placed anywhere and will run the monitor

cd /d "%~dp0"

:: Try to run the executable first (if built)
if exist "dist\DatecsCashRegisterMonitor.exe" (
    echo Starting Datecs Monitor from executable...
    start "" "dist\DatecsCashRegisterMonitor.exe"
    exit
)

:: If no executable, run from Python source
if exist "cash_register_monitor\main.py" (
    echo Starting Datecs Monitor from Python source...
    start /B pythonw cash_register_monitor/main.py
    echo Monitor started in system tray!
    timeout /t 3 >nul
    exit
)

echo ERROR: Cannot find Datecs Cash Register Monitor files.
echo Please make sure you're in the correct directory.
pause