@echo off
REM AI All-in-One Tool Startup Script for Windows

echo ========================================
echo AI All-in-One Data Tool - Startup
echo ========================================
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -r backend\requirements.txt > nul 2>&1

REM Create data directory
if not exist "data" mkdir data

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env > nul
    echo.
    echo IMPORTANT: Edit .env and add your ANTHROPIC_API_KEY
    echo.
)

REM Start backend
echo.
echo Starting backend server on http://localhost:8000
echo.
cd backend
python main.py
