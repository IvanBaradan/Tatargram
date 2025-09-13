#!/bin/bash
# startup.sh - Script to start the Telegram CRM service

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create a .env file with your Telegram credentials."
    echo "You can copy .env.example to .env and fill in your details."
    exit 1
fi

# Check if required environment variables are set
if [ -z "$TELEGRAM_API_ID" ] || [ -z "$TELEGRAM_API_HASH" ] || [ -z "$TELEGRAM_PHONE_NUMBER" ]; then
    echo "Warning: Required Telegram environment variables not set."
    echo "Please check your .env file."
fi

# Install dependencies if not already installed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Start the service
echo "Starting Telegram CRM service..."
python telegram_api/main.py