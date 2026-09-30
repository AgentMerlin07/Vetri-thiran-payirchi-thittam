@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo        LegalEase - Windows Setup
echo ==========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Install Python 3.10+ and try again.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Installing/updating dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt

if not exist ".env" (
    copy /Y ".env.example" ".env" >nul
    echo.
    echo Created .env from .env.example.
    echo Add your GEMINI_API_KEY before generating documents.
)

echo.
echo Setup complete.
echo.
echo Backend:  run_backend.bat
echo Frontend: run_frontend.bat
echo Tests:    test_backend.bat
echo.
pause
