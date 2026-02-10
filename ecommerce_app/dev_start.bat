@echo off
echo ===============================
echo Starting Ecommerce FastAPI App
echo ===============================

REM Go to project root (important if double-clicked)
cd /d "%~dp0"

REM Activate virtual environment
call venv\Scripts\activate

REM Run FastAPI using run.py
python run.py

pause
