#!/usr/bin/env python3
"""
Test script to verify the database fix works
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_import():
    """Test that we can import database components without SQLAlchemy errors"""
    print("Testing database import...")
    
    try:
        # This should not trigger the SQLAlchemy import error
        from app.core.database import get_db, create_tables
        print("✅ Database components imported successfully")
        return True
    except Exception as e:
        print(f"❌ Database import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_import():
    """Test that we can import the main app without SQLAlchemy errors"""
    print("Testing main app import...")
    
    try:
        # This should not trigger the SQLAlchemy import error
        from app.main import app
        print("✅ Main app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Main app import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_settings_import():
    """Test that we can import settings"""
    print("Testing settings import...")
    
    try:
        from app.core.config import settings
        print("✅ Settings imported successfully")
        print(f"App Name: {settings.APP_NAME}")
        print(f"CORS Origins: {settings.CORS_ORIGINS_LIST}")
        return True
    except Exception as e:
        print(f"❌ Settings import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running database fix verification tests...")
    print("=" * 50)
    
    success = True
    success &= test_settings_import()
    success &= test_database_import()
    success &= test_main_import()
    
    if success:
        print("\n🎉 All tests passed! The database fix is working.")
        print("\nYou can now run the backend with:")
        print("python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("\n💥 Some tests failed. Please check the errors above.")
        
    sys.exit(0 if success else 1)