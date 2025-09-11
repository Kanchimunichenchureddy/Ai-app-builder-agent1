#!/usr/bin/env python3
"""
Script to check if the backend server is running and provide start instructions if not
"""

import requests
import socket
import subprocess
import sys
import time
import os

def is_port_open(host, port):
    """Check if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def check_backend_server():
    """Check if backend server is running"""
    print("AI App Builder - Backend Server Status Check")
    print("=" * 45)
    
    # Check if port 8000 is open
    port_open = is_port_open('localhost', 8000)
    
    if port_open:
        print("✅ Port 8000: OPEN")
        # Try to access the backend
        try:
            response = requests.get('http://localhost:8000/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ Backend Server: RUNNING")
                print(f"   Message: {data.get('message', 'N/A')}")
                print(f"   Version: {data.get('version', 'N/A')}")
                return True
            else:
                print(f"⚠️  Backend Server: RESPONDING BUT STATUS {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Backend Server: NOT RESPONDING (port open but no HTTP server)")
            return False
        except Exception as e:
            print(f"❌ Backend Server: ERROR - {str(e)}")
            return False
    else:
        print("❌ Port 8000: CLOSED")
        print("❌ Backend Server: NOT RUNNING")
        return False

def provide_start_instructions():
    """Provide instructions on how to start the backend server"""
    print("\n" + "=" * 45)
    print("HOW TO START THE BACKEND SERVER:")
    print("=" * 45)
    
    backend_path = os.path.join(os.getcwd(), "backend")
    print(f"1. Open a new terminal/command prompt")
    print(f"2. Navigate to the backend directory:")
    print(f"   cd \"{backend_path}\"")
    print("3. Start the backend server using one of these methods:")
    print("   Option A - Direct command:")
    print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    print("\n   Option B - Using batch file (Windows):")
    print("   start_server.bat")
    print("\n   Option C - Using PowerShell script:")
    print("   .\\start_server.ps1")
    print("\n4. Wait for the message: \"Application startup complete.\"")
    print("5. Keep this terminal open while using the application")

def check_frontend_server():
    """Check if frontend server is running"""
    print("\n" + "=" * 45)
    print("FRONTEND SERVER STATUS:")
    print("=" * 45)
    
    # Check if port 3000 is open
    port_open = is_port_open('localhost', 3000)
    
    if port_open:
        print("✅ Port 3000: OPEN")
        print("✅ Frontend Server: LIKELY RUNNING")
        print("   Access at: http://localhost:3000")
    else:
        print("❌ Port 3000: CLOSED")
        print("❌ Frontend Server: NOT RUNNING")
        print("\nHOW TO START THE FRONTEND SERVER:")
        print("1. Open a new terminal/command prompt")
        print("2. Navigate to the frontend directory:")
        frontend_path = os.path.join(os.getcwd(), "frontend")
        print(f"   cd \"{frontend_path}\"")
        print("3. Install dependencies (if not already done):")
        print("   npm install")
        print("4. Start the frontend server:")
        print("   npm start")
        print("5. Wait for compilation to complete")
        print("6. Keep this terminal open while using the application")

def main():
    print("Checking AI App Builder server status...")
    print()
    
    backend_running = check_backend_server()
    check_frontend_server()
    
    if not backend_running:
        provide_start_instructions()
    
    print("\n" + "=" * 45)
    print("QUICK START COMMANDS:")
    print("=" * 45)
    print("To start backend in current terminal:")
    print("cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    print("\nTo start frontend in current terminal:")
    print("cd frontend && npm start")

if __name__ == "__main__":
    main()