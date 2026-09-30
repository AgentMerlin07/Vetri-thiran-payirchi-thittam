@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found.
    echo Run setup_windows.bat first.
    pause
    exit /b 1
)

echo Running LegalEase backend tests...
echo.
".venv\Scripts\python.exe" -m pytest -q
echo.
pause
