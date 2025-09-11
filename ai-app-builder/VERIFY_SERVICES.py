#!/usr/bin/env python3
"""
Script to verify that both frontend and backend services are running correctly
"""

import requests
import socket
import time

def check_port(host, port):
    """Check if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def check_backend():
    """Check if backend is running and responding"""
    try:
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
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {str(e)}")
        return False

def check_frontend():
    """Check if frontend is running (basic check)"""
    try:
        # For frontend, we'll just check if the port is open
        # since we can't easily check the React dev server response
        is_open = check_port('localhost', 3000)
        if is_open:
            print("✅ Frontend port (3000) is open - this means the frontend server is likely running")
            return True
        else:
            print("❌ Frontend port (3000) is not open - frontend may not be running")
            return False
    except Exception as e:
        print(f"❌ Error checking frontend: {str(e)}")
        return False

def check_cors():
    """Check if CORS is properly configured by testing an API endpoint"""
    try:
        response = requests.options('http://localhost:8000/api/ai/capabilities', 
                                  headers={'Origin': 'http://localhost:3000'},
                                  timeout=5)
        if response.status_code in [200, 204]:
            print("✅ CORS is properly configured for frontend-backend communication")
            return True
        else:
            print(f"⚠️  CORS check returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking CORS: {str(e)}")
        return False

def main():
    print("AI App Builder - Service Verification")
    print("=" * 50)
    
    print("\n1. Checking Backend Service (Port 8000)...")
    backend_ok = check_backend()
    
    print("\n2. Checking Frontend Service (Port 3000)...")
    frontend_ok = check_frontend()
    
    if backend_ok:
        print("\n3. Checking CORS Configuration...")
        check_cors()
    
    print("\n" + "=" * 50)
    print("ACCESS INSTRUCTIONS:")
    print("✅ Frontend Application: http://localhost:3000")
    print("✅ Backend API:          http://localhost:8000")
    print("✅ API Documentation:    http://localhost:8000/docs")
    
    print("\nREMINDERS:")
    print("⚠️  Do NOT use http://0.0.0.0:8000 in your browser")
    print("⚠️  Always use http://localhost:8000 for backend")
    print("⚠️  Always use http://localhost:3000 for frontend")
    
    if backend_ok and frontend_ok:
        print("\n🎉 Both services appear to be running correctly!")
        print("   Open http://localhost:3000 in your browser to see the frontend")
    elif backend_ok:
        print("\n⚠️  Backend is running, but frontend may not be")
        print("   Make sure you started the frontend with 'npm start'")
    elif frontend_ok:
        print("\n⚠️  Frontend appears to be running, but backend may not be")
        print("   Make sure you started the backend with the uvicorn command")
    else:
        print("\n❌ Neither service appears to be running correctly")
        print("   Please check your startup commands and try again")

if __name__ == "__main__":
    main()