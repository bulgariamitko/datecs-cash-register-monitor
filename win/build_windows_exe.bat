@echo off
echo ========================================
echo Building Datecs Cash Register Monitor
echo Windows Executable
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

:: Navigate to script directory
cd /d "%~dp0"

:: Install PyInstaller if not present
echo Checking for PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

:: Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"

echo.
echo Building executable...
echo This may take a few minutes...

:: Build the executable
pyinstaller ^
    --onefile ^
    --windowed ^
    --name=DatecsCashRegisterMonitor ^
    --icon=cash_register_monitor/icons/connected.ico ^
    --add-data="cash_register_monitor/icons;icons" ^
    --hidden-import=pystray._win32 ^
    --hidden-import=PIL._tkinter_finder ^
    --clean ^
    cash_register_monitor/main.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\DatecsCashRegisterMonitor.exe
echo File size: 
for %%A in ("dist\DatecsCashRegisterMonitor.exe") do echo %%~zA bytes

echo.
echo You can now:
echo 1. Run: dist\DatecsCashRegisterMonitor.exe
echo 2. Copy the exe file anywhere you want
echo 3. Add to Windows startup for automatic monitoring
echo.
pause