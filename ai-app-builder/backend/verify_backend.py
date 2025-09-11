#!/usr/bin/env python3
"""
Script to verify that the backend service is running correctly
This version is designed to run from within the backend directory
"""

import sys
import os

# Add the current directory to the path so we can import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_backend():
    """Check if backend is running and responding"""
    try:
        import requests
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is running!")
            print(f"   Message: {data.get('message', 'N/A')}")
            print(f"   Version: {data.get('version', 'N/A')}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not accessible - make sure it's running")
        print("   Start it with: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {str(e)}")
        return False

def check_health():
    """Check backend health endpoint"""
    try:
        import requests
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend health check passed!")
            print(f"   Status: {data.get('status', 'N/A')}")
            print(f"   Database: {data.get('database', 'N/A')}")
            return True
        else:
            print(f"❌ Health check returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking health: {str(e)}")
        return False

def main():
    print("AI App Builder - Backend Verification")
    print("=" * 40)
    
    print("\n1. Checking Backend Service...")
    backend_ok = check_backend()
    
    if backend_ok:
        print("\n2. Checking Health Endpoint...")
        check_health()
    
    print("\n" + "=" * 40)
    print("ACCESS INSTRUCTIONS:")
    print("✅ Backend API:       http://localhost:8000")
    print("✅ API Documentation: http://localhost:8000/docs")
    
    print("\nREMINDERS:")
    print("⚠️  Do NOT use http://0.0.0.0:8000 in your browser")
    print("⚠️  Always use http://localhost:8000 for backend access")
    
    if backend_ok:
        print("\n🎉 Backend service is running correctly!")
    else:
        print("\n❌ Backend service is not running correctly")
        print("   Please start the backend with:")
        print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")

if __name__ == "__main__":
    # Try to import requests, if it fails, inform the user
    try:
        import requests
    except ImportError:
        print("❌ 'requests' module not found.")
        print("   Please install it with: pip install requests")
        sys.exit(1)
        
    main()