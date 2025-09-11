#!/usr/bin/env python3
"""
Script to start backend services with proper error handling
"""
import os
import sys

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("Checking prerequisites...")
    
    # Check if required environment variables are set
    required_vars = [
        "OPENAI_API_KEY",
        "DB_HOST",
        "DB_USER",
        "DB_PASSWORD",
        "DB_NAME"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {missing_vars}")
        return False
    
    print("✅ All prerequisites met!")
    return True

def start_backend():
    """Start the backend service"""
    try:
        print("Starting backend service...")
        
        # Import and initialize the app
        from app.main import app
        
        print("✅ Backend app initialized successfully!")
        print("✅ FastAPI app is ready to serve requests!")
        
        # Print configuration details
        from app.core.config import settings
        print(f"   App Name: {settings.APP_NAME}")
        print(f"   Version: {settings.VERSION}")
        print(f"   Debug Mode: {settings.DEBUG}")
        print(f"   CORS Origins: {settings.CORS_ORIGINS_LIST}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("AI App Builder - Backend Service Starter")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        print("Please configure your environment variables in the .env file")
        sys.exit(1)
    
    # Start backend
    if start_backend():
        print("\n" + "=" * 50)
        print("🎉 Backend service is ready!")
        print("You can now start the server with:")
        print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("\n" + "=" * 50)
        print("💥 Failed to start backend service!")
        sys.exit(1)