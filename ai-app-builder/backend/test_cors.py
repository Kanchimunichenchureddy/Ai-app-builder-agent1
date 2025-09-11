import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app.core.config import settings
    print("Config loaded successfully!")
    print(f"CORS Origins String: {settings.CORS_ORIGINS}")
    print(f"CORS Origins List: {settings.CORS_ORIGINS_LIST}")
except Exception as e:
    print(f"Error loading config: {e}")
    import traceback
    traceback.print_exc()