@echo off

:: PMS Voting System - Stop Server Script
:: This script safely stops all running instances of the voting system

echo ========================================
echo    PMS Voting System - Stop Server
echo ========================================
echo.

echo Stopping PMS Voting System server...

:: Kill Python processes running app.py
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo csv ^| findstr "python.exe"') do (
    for /f "tokens=2 delims=," %%j in ("%%i") do (
        set PID=%%j
        set PID=!PID:"=!
        
        :: Check if this Python process is running our app
        wmic process where "ProcessId=!PID!" get CommandLine /format:list 2>nul | findstr /i "app.py" >nul
        if !errorlevel! equ 0 (
            echo Stopping Python process with PID: !PID!
            taskkill /pid !PID! /f >nul 2>&1
        )
    )
)

:: Also try to kill any process using port 5000
echo Checking for processes using port 5000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000"') do (
    set PID=%%a
    if not "!PID!"=="" (
        echo Stopping process using port 5000 (PID: !PID!)
        taskkill /pid !PID! /f >nul 2>&1
    )
)

:: Kill any remaining Flask development servers
taskkill /f /im "python.exe" /fi "windowtitle eq PMS Voting System Server" >nul 2>&1

echo.
echo ========================================
echo    All server processes have been stopped
echo ========================================
echo.
echo Port 5000 is now free
echo You can now start the server again if needed
echo.

timeout /t 3 /nobreak >nul
