@echo off
setlocal enabledelayedexpansion

:: PMS Voting System - Developer Run Script
:: This script sets up and runs the application with console output visible

echo ========================================
echo    PMS Voting System - Developer Mode
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

echo [1/5] Checking Python installation...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

:: Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo [2/5] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
) else (
    echo [2/5] Virtual environment already exists
)

:: Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated

:: Upgrade pip
echo [4/5] Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies
echo [5/5] Installing/checking dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo WARNING: Failed to install from requirements.txt
    echo Trying to install Flask manually...
    pip install Flask==2.3.3 Werkzeug==2.3.7
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install Flask
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo      Setup Complete! Starting Server...
echo ========================================
echo.
echo The application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

:: Wait a moment
timeout /t 2 /nobreak >nul

:: Start the application
python app.py

echo.
echo ========================================
echo         Server has stopped
echo ========================================
echo.
pause
