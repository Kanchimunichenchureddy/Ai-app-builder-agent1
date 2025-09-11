import os
import sys

# Add the backend directory to the Python path
backend_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_path)

print("Current working directory:", os.getcwd())
print("Backend path:", backend_path)

try:
    # Import and test the config
    from app.core.config import settings
    print("✅ Config loaded successfully!")
    print(f"✅ App Name: {settings.APP_NAME}")
    print(f"✅ CORS Origins String: {settings.CORS_ORIGINS}")
    print(f"✅ CORS Origins List: {settings.CORS_ORIGINS_LIST}")
    print("✅ All configurations are working correctly!")
except Exception as e:
    print(f"❌ Error loading config: {e}")
    import traceback
    traceback.print_exc()