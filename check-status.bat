@echo off

:: PMS Voting System - Check Status Script
:: This script checks if the voting system is running

echo ========================================
echo    PMS Voting System - Status Check
echo ========================================
echo.

:: Check if virtual environment exists
if exist "venv\" (
    echo [✓] Virtual environment: EXISTS
) else (
    echo [✗] Virtual environment: NOT FOUND
)

:: Check if dependencies are installed
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat >nul 2>&1
    pip show Flask >nul 2>&1
    if !errorlevel! equ 0 (
        echo [✓] Flask dependency: INSTALLED
    ) else (
        echo [✗] Flask dependency: NOT INSTALLED
    )
) else (
    echo [✗] Cannot check dependencies: Virtual environment not found
)

:: Check if database exists
if exist "voting_system.db" (
    echo [✓] Database file: EXISTS
) else (
    echo [✗] Database file: NOT FOUND (will be created on first run)
)

:: Check if server is running
echo.
echo Checking if server is running on port 5000...
netstat -an | findstr ":5000" >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] Server: RUNNING on port 5000
    echo     Access at: http://localhost:5000
) else (
    echo [✗] Server: NOT RUNNING
)

:: Check for Python processes running app.py
echo.
echo Checking for PMS Voting System processes...
set FOUND_PROCESS=0
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo csv 2^>nul ^| findstr "python.exe"') do (
    for /f "tokens=2 delims=," %%j in ("%%i") do (
        set PID=%%j
        set PID=!PID:"=!
        
        wmic process where "ProcessId=!PID!" get CommandLine /format:list 2>nul | findstr /i "app.py" >nul
        if !errorlevel! equ 0 (
            echo [✓] Found PMS process: PID !PID!
            set FOUND_PROCESS=1
        )
    )
)

if %FOUND_PROCESS% equ 0 (
    echo [✗] No PMS Voting System processes found
)

echo.
echo ========================================
echo            Status Summary
echo ========================================
echo.
echo To setup the system: Double-click 'setup-only.bat'
echo To start the system: Double-click 'quick-start.bat' or 'run.bat'
echo To stop the system:  Double-click 'stop-server.bat'
echo.

pause
