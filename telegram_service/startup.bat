@echo off
REM startup.bat - Script to start the Telegram CRM service on Windows

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found!
    echo Please create a .env file with your Telegram credentials.
    echo You can copy .env.example to .env and fill in your details.
    pause
    exit /b 1
)

REM Check if required environment variables are set
if "%TELEGRAM_API_ID%"=="" (
    echo Warning: TELEGRAM_API_ID environment variable not set.
    echo Please check your .env file.
)

if "%TELEGRAM_API_HASH%"=="" (
    echo Warning: TELEGRAM_API_HASH environment variable not set.
    echo Please check your .env file.
)

if "%TELEGRAM_PHONE_NUMBER%"=="" (
    echo Warning: TELEGRAM_PHONE_NUMBER environment variable not set.
    echo Please check your .env file.
)

REM Install dependencies if not already installed
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Start the service
echo Starting Telegram CRM service...
python telegram_api/main.py

pause