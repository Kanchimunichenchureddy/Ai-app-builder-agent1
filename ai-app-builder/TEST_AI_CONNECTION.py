#!/usr/bin/env python3
"""
Script to test the connection between frontend and backend for AI chat functionality
"""

import requests
import json
import sys
import time

def test_backend_connection():
    """Test if backend is accessible"""
    try:
        response = requests.get('http://localhost:8000/', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend Server: RUNNING")
            print(f"   Message: {data.get('message', 'N/A')}")
            print(f"   Version: {data.get('version', 'N/A')}")
            return True
        else:
            print(f"❌ Backend Server: RETURNED STATUS {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend Server: NOT ACCESSIBLE")
        print("   Please make sure the backend server is running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Backend Server: ERROR - {str(e)}")
        return False

def test_backend_health():
    """Test backend health endpoint"""
    try:
        response = requests.get('http://localhost:8000/health', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend Health: OK")
            print(f"   Status: {data.get('status', 'N/A')}")
            print(f"   Database: {data.get('database', 'N/A')}")
            return True
        else:
            print(f"❌ Backend Health: RETURNED STATUS {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend Health: ERROR - {str(e)}")
        return False

def test_ai_endpoints():
    """Test AI-related endpoints"""
    try:
        # Test capabilities endpoint (correct path is /api/builder/capabilities)
        response = requests.get('http://localhost:8000/api/builder/capabilities', timeout=10)
        if response.status_code == 200:
            print("✅ AI Capabilities Endpoint: ACCESSIBLE")
            data = response.json()
            if 'capabilities' in data:
                print(f"   Available Capabilities: {len(data['capabilities'])}")
        elif response.status_code == 404:
            print("⚠️  AI Capabilities Endpoint: NOT FOUND")
        else:
            print(f"❌ AI Capabilities Endpoint: RETURNED STATUS {response.status_code}")
    except Exception as e:
        print(f"❌ AI Capabilities Endpoint: ERROR - {str(e)}")

def test_cors():
    """Test CORS configuration by making a preflight request to the correct endpoint"""
    try:
        response = requests.options('http://localhost:8000/api/builder/capabilities', 
                                  headers={'Origin': 'http://localhost:3000',
                                           'Access-Control-Request-Method': 'GET'},
                                  timeout=10)
        if response.status_code in [200, 204]:
            print("✅ CORS Configuration: PROPERLY CONFIGURED")
            allow_origin = response.headers.get('access-control-allow-origin', 'Not set')
            print(f"   Allowed Origins: {allow_origin}")
        else:
            print(f"❌ CORS Configuration: RETURNED STATUS {response.status_code}")
    except Exception as e:
        print(f"❌ CORS Configuration: ERROR - {str(e)}")

def test_ai_chat():
    """Test AI chat functionality - this requires authentication so we'll just check if endpoint exists"""
    try:
        # Test if the endpoint exists by making an OPTIONS request (preflight)
        response = requests.options('http://localhost:8000/api/builder/chat', 
                                  headers={'Origin': 'http://localhost:3000',
                                           'Access-Control-Request-Method': 'POST'},
                                  timeout=10)
        
        if response.status_code in [200, 204, 405]:
            print("✅ AI Chat Endpoint: EXISTS")
            if response.status_code == 405:
                # 405 means method not allowed, but endpoint exists
                print("   Note: POST method required for chat (405 is expected for OPTIONS)")
        elif response.status_code == 404:
            print("❌ AI Chat Endpoint: NOT FOUND")
        else:
            print(f"⚠️  AI Chat Endpoint: RETURNED STATUS {response.status_code}")
    except Exception as e:
        print(f"❌ AI Chat Endpoint Test: ERROR - {str(e)}")

def main():
    print("AI App Builder - Connection Test")
    print("=" * 35)
    print("Testing connection between frontend and backend for AI chat functionality")
    print()
    
    print("1. Testing Backend Server...")
    backend_ok = test_backend_connection()
    
    if backend_ok:
        print("\n2. Testing Backend Health...")
        test_backend_health()
        
        print("\n3. Testing AI Endpoints...")
        test_ai_endpoints()
        
        print("\n4. Testing CORS Configuration...")
        test_cors()
        
        print("\n5. Testing AI Chat Endpoint...")
        test_ai_chat()
    
    print("\n" + "=" * 35)
    print("ACCESS URLs:")
    print("✅ Frontend Application: http://localhost:3000")
    print("✅ Backend API: http://localhost:8000")
    print("✅ API Documentation: http://localhost:8000/docs")
    
    print("\nREMINDERS:")
    print("⚠️  Do NOT use http://0.0.0.0:8000 in your browser")
    print("⚠️  Always use http://localhost:8000 for backend access")
    print("⚠️  Keep both terminal windows open while using the application")
    print("⚠️  AI chat requires authentication - login first in the frontend")

if __name__ == "__main__":
    main()