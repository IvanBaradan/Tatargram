"""
Database initialization script
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram_client.models import create_tables

if __name__ == "__main__":
    print("Initializing Telegram database...")
    engine = create_tables()
    print("Database initialized successfully!")
    print(f"Database URL: {engine.url}")