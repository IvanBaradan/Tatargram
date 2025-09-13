"""
Dependency check script
"""
import sys
import importlib

def check_dependency(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✓ {package_name} is installed")
        return True
    except ImportError:
        print(f"✗ {package_name} is NOT installed")
        return False

def main():
    print("Checking Telegram CRM service dependencies...")
    print("=" * 50)
    
    dependencies = [
        ("Telethon", "telethon"),
        ("FastAPI", "fastapi"),
        ("Uvicorn", "uvicorn"),
        ("SQLAlchemy", "sqlalchemy"),
        ("python-dotenv", "dotenv"),
        ("aiohttp", "aiohttp"),
        ("websockets", "websockets"),
        ("Pillow", "PIL"),
    ]
    
    all_good = True
    for package_name, import_name in dependencies:
        if not check_dependency(package_name, import_name):
            all_good = False
    
    print("=" * 50)
    if all_good:
        print("All dependencies are installed! ✓")
        print("You can now run the Telegram CRM service.")
    else:
        print("Some dependencies are missing! ✗")
        print("Please install them using: pip install -r requirements.txt")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)