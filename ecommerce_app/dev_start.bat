@echo off
echo ===============================
echo Installing Requirements
echo ===============================

REM Go to project root (important if double-clicked)
cd /d "%~dp0"

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r app\config\requirements.txt

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Failed to install requirements.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ===============================
echo Starting Ecommerce FastAPI App
echo ===============================

REM Run FastAPI
python run.py

pause
