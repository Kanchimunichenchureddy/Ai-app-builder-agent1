import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from backend.app.main import app
    print("✅ FastAPI app imported successfully")
    
    # Test importing database
    from backend.app.core.database import engine, SessionLocal, Base
    print("✅ Database components imported successfully")
    
    # Test importing models
    from backend.app.models.user import User
    print("✅ User model imported successfully")
    
    print("\n✅ All imports successful! The server should start correctly.")
    print("\nTo start the server, run:")
    print("cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    
except Exception as e:
    print(f"❌ Error importing components: {e}")
    import traceback
    traceback.print_exc()