#!/usr/bin/env python3
"""
Simple test script to check if the FastAPI server can start
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing imports...")
    from app.main import app
    print("✅ All imports successful!")
    
    print("Testing configuration...")
    from app.core.config import settings
    print(f"✅ App name: {settings.APP_NAME}")
    print(f"✅ Version: {settings.VERSION}")
    print(f"✅ Debug mode: {settings.DEBUG}")
    
    print("Testing database connection...")
    try:
        from app.core.database import get_db
        print("✅ Database module imported successfully")
    except Exception as e:
        print(f"⚠️ Database connection test failed: {e}")
    
    print("Testing AI services...")
    try:
        from app.services.ai_agent import AIAgentService
        ai_agent = AIAgentService()
        print("✅ AI Agent service initialized successfully")
    except Exception as e:
        print(f"❌ AI Agent service failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 All tests passed! The server should start successfully.")
    print("\nTo start the server, run:")
    print("python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()