import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing configuration...")
    
    # Test config import
    from app.core.config import settings
    print("✓ Config imported successfully")
    print(f"  App Name: {settings.APP_NAME}")
    print(f"  Database URL: {settings.DATABASE_URL}")
    print(f"  CORS Origins String: {settings.CORS_ORIGINS}")
    print(f"  CORS Origins List: {settings.CORS_ORIGINS_LIST}")
    print(f"  Debug Mode: {settings.DEBUG}")
    
    # Test that CORS_ORIGINS_LIST is a list
    if isinstance(settings.CORS_ORIGINS_LIST, list):
        print("✓ CORS_ORIGINS_LIST is properly configured as a list")
        for origin in settings.CORS_ORIGINS_LIST:
            print(f"  - {origin}")
    else:
        print(f"❌ CORS_ORIGINS_LIST is not a list: {type(settings.CORS_ORIGINS_LIST)}")
        
    print("\n🎉 Configuration test passed!")
    
except Exception as e:
    print(f"❌ Error during configuration test: {e}")
    import traceback
    traceback.print_exc()