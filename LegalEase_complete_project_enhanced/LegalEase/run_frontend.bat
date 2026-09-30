@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found.
    echo Run setup_windows.bat first.
    pause
    exit /b 1
)

echo Starting LegalEase Streamlit frontend...
echo URL: http://localhost:8501
echo.
".venv\Scripts\python.exe" -m streamlit run app.py
