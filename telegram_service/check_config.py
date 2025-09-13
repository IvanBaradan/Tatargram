"""
Configuration checker
"""
import os
from config import config

def check_config():
    """Check configuration and environment variables"""
    print("Telegram CRM Service - Configuration Check")
    print("=" * 50)
    
    # Check required environment variables
    required_vars = {
        'TELEGRAM_API_ID': config.TELEGRAM_API_ID,
        'TELEGRAM_API_HASH': config.TELEGRAM_API_HASH,
        'TELEGRAM_PHONE_NUMBER': config.TELEGRAM_PHONE_NUMBER
    }
    
    all_good = True
    
    print("Required Environment Variables:")
    for var_name, var_value in required_vars.items():
        if var_value:
            print(f"  ✓ {var_name}: {'*' * len(str(var_value)) if 'API' in var_name else var_value}")
        else:
            print(f"  ✗ {var_name}: NOT SET")
            all_good = False
    
    print("\nOptional Configuration:")
    optional_vars = {
        'DATABASE_URL': config.DATABASE_URL,
        'HOST': config.HOST,
        'PORT': config.PORT,
        'SESSION_FILE': config.SESSION_FILE
    }
    
    for var_name, var_value in optional_vars.items():
        print(f"  {var_name}: {var_value}")
    
    print("\n" + "=" * 50)
    if all_good:
        print("Configuration is complete! ✓")
        print("You can now run the Telegram CRM service.")
    else:
        print("Configuration is incomplete! ✗")
        print("Please set the required environment variables.")
        print("You can copy .env.example to .env and fill in your details.")
    
    return all_good

if __name__ == "__main__":
    success = check_config()
    exit(0 if success else 1)