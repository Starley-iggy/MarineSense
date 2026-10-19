@echo off
title MarineSense Dashboard
cd /d "%~dp0"

REM Create a local Python environment if it does not exist yet.
if not exist ".venv\Scripts\python.exe" (
    echo Creating Python virtual environment...
    py -m venv .venv
    if errorlevel 1 (
        echo Could not create the environment. Is Python installed?
        pause
        exit /b 1
    )
)

REM Install the required packages in this project's own environment.
echo Installing/checking dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Package installation failed. Check your internet connection and Python setup.
    pause
    exit /b 1
)

REM Start the dashboard. Keep this window open while using the app.
echo Starting MarineSense...
".venv\Scripts\python.exe" -m streamlit run app.py
pause
