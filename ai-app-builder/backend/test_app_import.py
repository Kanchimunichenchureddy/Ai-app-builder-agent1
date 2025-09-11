import os
import sys

# Add the backend directory to the Python path
backend_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_path)

print("Testing app import...")

try:
    # Import the main app
    from app.main import app
    print("✅ App imported successfully!")
    print("✅ FastAPI app is working correctly!")
    
    # Test accessing the settings
    from app.core.config import settings
    print(f"✅ App Name: {settings.APP_NAME}")
    print(f"✅ CORS Origins: {settings.CORS_ORIGINS_LIST}")
    
    print("\n🎉 All tests passed! The backend should start correctly now.")
    
except Exception as e:
    print(f"❌ Error importing app: {e}")
    import traceback
    traceback.print_exc()