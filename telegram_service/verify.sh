#!/bin/bash
# Verification script for Telegram CRM Service

echo "Telegram CRM Service - Verification Script"
echo "========================================"
echo

echo "1. Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python not found"
    exit 1
fi

echo
echo "2. Checking dependencies..."
python3 check_deps.py
if [ $? -ne 0 ]; then
    echo "Error: Dependency check failed"
    exit 1
fi

echo
echo "3. Checking configuration..."
python3 check_config.py
if [ $? -ne 0 ]; then
    echo "Error: Configuration check failed"
    exit 1
fi

echo
echo "4. Initializing database..."
python3 init_db.py
if [ $? -ne 0 ]; then
    echo "Error: Database initialization failed"
    exit 1
fi

echo
echo "========================================"
echo "Verification completed successfully! ✓"
echo
echo "You can now run the service with:"
echo "  python3 telegram_api/main.py"
echo
echo "And access the frontend at:"
echo "  telegram_frontend/index.html"