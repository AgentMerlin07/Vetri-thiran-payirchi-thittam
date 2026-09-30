@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found.
    echo Run setup_windows.bat first.
    pause
    exit /b 1
)

echo Starting LegalEase FastAPI backend...
echo API:   http://127.0.0.1:8000
echo Docs:  http://127.0.0.1:8000/docs
echo Health:http://127.0.0.1:8000/health
echo.
".venv\Scripts\python.exe" -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
