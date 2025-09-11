#!/usr/bin/env python3
"""
Final test to verify the CORS configuration fix
"""
import os
import sys

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def test_config():
    """Test that the configuration loads without errors"""
    try:
        print("Testing configuration loading...")
        
        # This should trigger the error if it still exists
        from app.core.config import settings
        
        print("✅ Configuration loaded successfully!")
        print(f"✅ App Name: {settings.APP_NAME}")
        print(f"✅ CORS Origins String: {settings.CORS_ORIGINS}")
        print(f"✅ CORS Origins List: {settings.CORS_ORIGINS_LIST}")
        
        # Test that the list is properly formed
        if isinstance(settings.CORS_ORIGINS_LIST, list) and len(settings.CORS_ORIGINS_LIST) > 0:
            print("✅ CORS Origins List is properly formatted")
            for origin in settings.CORS_ORIGINS_LIST:
                print(f"   - {origin}")
        else:
            print("❌ CORS Origins List is not properly formatted")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_config()
    if success:
        print("\n🎉 All tests passed! The CORS configuration issue should be fixed.")
        sys.exit(0)
    else:
        print("\n💥 Tests failed. The CORS configuration issue still exists.")
        sys.exit(1)