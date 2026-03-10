@echo off
REM Quick Start Script for Insurance Dashboard (Windows)

echo ==========================================
echo Medical Insurance Dashboard - Quick Start
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [✓] Python found

REM Install requirements
echo.
echo Installing required packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [✓] Dependencies installed successfully

REM Launch dashboard
echo.
echo ==========================================
echo Launching Streamlit Dashboard...
echo ==========================================
echo.
echo The dashboard will open in your default browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

streamlit run dashboard.py
pause
