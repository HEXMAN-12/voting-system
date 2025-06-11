@echo off
setlocal enabledelayedexpansion

:: PMS Voting System - Quick Start Script
:: This script sets up everything and opens the application automatically

echo ========================================
echo    PMS Voting System - Quick Start
echo ========================================
echo.

:: Change to script directory
cd /d "%~dp0"

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo [1/6] Checking Python installation...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

:: Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo [2/6] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
) else (
    echo [2/6] Virtual environment already exists
)

:: Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

:: Upgrade pip
echo [4/6] Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

:: Install dependencies
echo [5/6] Installing dependencies...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo Trying to install Flask manually...
    pip install Flask==2.3.3 Werkzeug==2.3.7
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install Flask
        pause
        exit /b 1
    )
)

:: Start the application in background
echo [6/6] Starting PMS Voting System...
echo.
echo ========================================
echo   Starting server in background...
echo   Opening web browser automatically...
echo ========================================
echo.

:: Start the server in a minimized window
start "PMS Voting System Server" /min cmd /c "call venv\Scripts\activate.bat && python app.py"

:: Wait a moment for server to start
timeout /t 3 /nobreak >nul

:: Open browser
start http://localhost:5000

echo.
echo ========================================
echo     PMS Voting System is now running!
echo ========================================
echo.
echo The application is running at: http://localhost:5000
echo Server is running in background (minimized window)
echo.
echo To stop the server:
echo - Double-click 'stop-server.bat'
echo - Or press Ctrl+C in the server window
echo.
echo Enjoy voting!
echo.

:: Keep this window open briefly to show status
timeout /t 5 /nobreak >nul

exit
