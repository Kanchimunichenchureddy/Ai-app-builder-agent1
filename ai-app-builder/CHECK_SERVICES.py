#!/usr/bin/env python3
"""
Script to check if all required services are running properly
"""

import socket
import subprocess
import sys
import os
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

def check_backend_api():
    """Check if backend API is responding"""
    try:
        import requests
        response = requests.get('http://localhost:8000/', timeout=5)
        return response.status_code == 200
    except:
        return False

def check_frontend():
    """Check if frontend is responding"""
    try:
        import requests
        response = requests.get('http://localhost:3000/', timeout=5)
        return response.status_code == 200
    except:
        return False

def check_env_file():
    """Check if .env file exists and has required keys"""
    env_path = os.path.join('backend', '.env')
    if not os.path.exists(env_path):
        return False, ".env file not found"
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
            if 'OPENROUTER_API_KEY' not in content:
                return False, "OPENROUTER_API_KEY not found in .env"
            if 'CORS_ORIGINS' not in content:
                return False, "CORS_ORIGINS not found in .env"
            return True, "All required keys found"
    except Exception as e:
        return False, f"Error reading .env file: {str(e)}"

def main():
    print("AI App Builder - Service Check")
    print("=" * 40)
    
    # Check .env file
    print("1. Checking .env configuration...")
    env_ok, env_msg = check_env_file()
    if env_ok:
        print(f"   ✅ {env_msg}")
    else:
        print(f"   ❌ {env_msg}")
    
    # Check ports
    print("\n2. Checking if required ports are open...")
    
    backend_port_open = check_port('localhost', 8000)
    if backend_port_open:
        print("   ✅ Backend port (8000) is open")
    else:
        print("   ❌ Backend port (8000) is closed - Backend server may not be running")
    
    frontend_port_open = check_port('localhost', 3000)
    if frontend_port_open:
        print("   ✅ Frontend port (3000) is open")
    else:
        print("   ❌ Frontend port (3000) is closed - Frontend may not be running")
    
    # Check API responses
    print("\n3. Checking API responses...")
    
    if backend_port_open:
        backend_api_ok = check_backend_api()
        if backend_api_ok:
            print("   ✅ Backend API is responding")
        else:
            print("   ❌ Backend API is not responding")
    else:
        print("   ⚠️  Skipping backend API check (port closed)")
    
    if frontend_port_open:
        frontend_ok = check_frontend()
        if frontend_ok:
            print("   ✅ Frontend is responding")
        else:
            print("   ❌ Frontend is not responding")
    else:
        print("   ⚠️  Skipping frontend check (port closed)")
    
    # Summary
    print("\n" + "=" * 40)
    print("SUMMARY:")
    
    issues = []
    if not env_ok:
        issues.append("Missing or invalid .env configuration")
    if not backend_port_open:
        issues.append("Backend server not running (port 8000)")
    if not frontend_port_open:
        issues.append("Frontend not running (port 3000)")
    
    if not issues:
        print("🎉 All services appear to be running correctly!")
        print("\nAccess your application at:")
        print("  Frontend: http://localhost:3000")
        print("  Backend:  http://localhost:8000")
        print("  Docs:     http://localhost:8000/docs")
    else:
        print("⚠️  Issues detected:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print("\nPlease check the FIX_INSTRUCTIONS.md file for troubleshooting steps.")

if __name__ == "__main__":
    main()