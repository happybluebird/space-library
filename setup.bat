@echo off
echo.
echo =========================================
echo   Space Library v6.0 - Setup
echo =========================================
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found.
    echo Install from: https://www.python.org/downloads/
    echo CHECK "Add Python to PATH" during setup!
    pause
    exit /b 1
)
echo [1/2] Installing packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Installation failed.
    pause
    exit /b 1
)
echo.
echo [2/2] Done!
echo.
echo =========================================
echo   Next:
echo   1. Open .streamlit\secrets.toml
echo      and enter your API keys
echo   2. Double-click run.bat
echo =========================================
echo.
pause
