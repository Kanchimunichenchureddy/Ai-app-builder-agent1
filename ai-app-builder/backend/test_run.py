#!/usr/bin/env python3
"""
Test script to manually run the FastAPI application
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    print("Testing imports...")
    try:
        from app.main import app
        print("✅ Main app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import main app: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    print("\nTesting config...")
    try:
        from app.core.config import settings
        print("✅ Config imported successfully")
        print(f"App name: {settings.APP_NAME}")
        print(f"CORS origins: {settings.CORS_ORIGINS_LIST}")
        return True
    except Exception as e:
        print(f"❌ Failed to import config: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database():
    print("\nTesting database...")
    try:
        from app.core.database import db_initialized, engine, SessionLocal, Base
        print(f"✅ Database module imported successfully")
        print(f"Database initialized: {db_initialized}")
        if engine:
            print(f"Engine: {engine}")
        return True
    except Exception as e:
        print(f"❌ Failed to import database: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("AI App Builder Backend Test Runner")
    print("=" * 50)
    
    # Test components
    import_success = test_imports()
    config_success = test_config()
    db_success = test_database()
    
    if import_success and config_success:
        print("\n" + "=" * 50)
        print("✅ Basic components loaded successfully!")
        print("You can now try running: uvicorn app.main:app --host 127.0.0.1 --port 8000")
    else:
        print("\n" + "=" * 50)
        print("❌ Some components failed to load")
        print("Check the errors above for troubleshooting")

if __name__ == "__main__":
    main()