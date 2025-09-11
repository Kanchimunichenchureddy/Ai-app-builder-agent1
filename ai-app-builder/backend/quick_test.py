import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test the settings import
try:
    from app.core.config import settings
    print("SUCCESS: Settings loaded correctly")
    print(f"App Name: {settings.APP_NAME}")
    print(f"CORS Origins String: {settings.CORS_ORIGINS}")
    print(f"CORS Origins List: {settings.CORS_ORIGINS_LIST}")
    print(f"Database URL: {settings.DATABASE_URL}")
    print("All settings loaded successfully!")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()