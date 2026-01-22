@echo off
cd /d "%~dp0"
start /B python cash_register_monitor/main.py
echo Datecs Cash Register Monitor started in background
timeout /t 2 >nul
exit