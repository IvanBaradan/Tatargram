@echo off
REM Verification script for Telegram CRM Service

echo Telegram CRM Service - Verification Script
echo ========================================
echo.

echo 1. Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo Error: Python not found
    pause
    exit /b 1
)

echo.
echo 2. Checking dependencies...
python check_deps.py
if %errorlevel% neq 0 (
    echo Error: Dependency check failed
    pause
    exit /b 1
)

echo.
echo 3. Checking configuration...
python check_config.py
if %errorlevel% neq 0 (
    echo Error: Configuration check failed
    pause
    exit /b 1
)

echo.
echo 4. Initializing database...
python init_db.py
if %errorlevel% neq 0 (
    echo Error: Database initialization failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Verification completed successfully! ✓
echo.
echo You can now run the service with:
echo   python telegram_api/main.py
echo.
echo And access the frontend at:
echo   telegram_frontend/index.html
echo.
pause