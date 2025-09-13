#!/usr/bin/env python3
"""
Setup script for Telegram CRM Service
"""
import os
import sys
import subprocess
import shutil

def check_python_version():
    """Check if Python 3.7+ is installed"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7+ is required")
        return False
    return True

def check_pip():
    """Check if pip is installed"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        print("Error: pip is not installed")
        return False

def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            shutil.copy(".env.example", ".env")
            print("✓ Created .env file from .env.example")
            print("Please edit .env to add your Telegram credentials")
            return True
        else:
            print("Error: .env.example file not found")
            return False
    return True

def install_dependencies():
    """Install Python dependencies"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def initialize_database():
    """Initialize the database"""
    try:
        subprocess.run([sys.executable, "init_db.py"], check=True)
        print("✓ Database initialized successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error initializing database: {e}")
        return False

def main():
    print("Telegram CRM Service - Setup Script")
    print("=" * 40)
    
    # Check prerequisites
    if not check_python_version():
        return False
        
    if not check_pip():
        return False
    
    # Create environment file
    if not create_env_file():
        return False
    
    # Install dependencies
    print("\nInstalling dependencies...")
    if not install_dependencies():
        return False
    
    # Initialize database
    print("\nInitializing database...")
    if not initialize_database():
        return False
    
    print("\n" + "=" * 40)
    print("Setup completed successfully! ✓")
    print("\nNext steps:")
    print("1. Edit .env file to add your Telegram credentials")
    print("2. Run 'python demonstrate.py' to test the connection")
    print("3. Run 'python telegram_api/main.py' to start the service")
    print("4. Open telegram_frontend/index.html in a browser")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)