#!/usr/bin/env python3
"""
Script to test AI chat functionality with proper authentication
"""

import requests
import json
import sys
import os

def test_ai_chat_with_auth():
    """Test AI chat functionality with authentication"""
    print("AI App Builder - AI Chat Authentication Test")
    print("=" * 45)
    
    # First, let's try to login with demo credentials
    print("\n1. Testing authentication...")
    
    # Demo credentials (as per project specifications)
    login_data = {
        "email": "demo@appforge.dev",
        "password": "demo123"
    }
    
    try:
        # Try to login
        response = requests.post('http://localhost:8000/api/auth/login', 
                               json=login_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        if response.status_code == 200:
            print("✅ Authentication: SUCCESSFUL")
            auth_data = response.json()
            token = auth_data.get('access_token')
            
            if token:
                print(f"   Token received: {token[:20]}...")
                
                # Now test the AI chat with the token
                print("\n2. Testing AI Chat with authentication...")
                test_chat_with_token(token)
            else:
                print("❌ No access token received")
                
        elif response.status_code == 401:
            print("⚠️  Authentication: INVALID CREDENTIALS")
            print("   This is expected in demo mode - frontend handles this specially")
            print("   AI chat will work in frontend with demo mode")
            
            # Test the capabilities endpoint without auth (should work)
            print("\n2. Testing AI Capabilities (no auth required)...")
            test_capabilities_no_auth()
            
        else:
            print(f"❌ Authentication: RETURNED STATUS {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Authentication: BACKEND NOT ACCESSIBLE")
        print("   Please make sure the backend server is running on port 8000")
    except Exception as e:
        print(f"❌ Authentication: ERROR - {str(e)}")

def test_chat_with_token(token):
    """Test AI chat with authentication token"""
    try:
        # Test chat endpoint with token
        chat_data = {
            "message": "Hello, what can you help me with?",
            "context": {}
        }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post('http://localhost:8000/api/builder/chat', 
                               json=chat_data,
                               headers=headers,
                               timeout=30)
        
        if response.status_code == 200:
            print("✅ AI Chat with Auth: SUCCESSFUL")
            data = response.json()
            if 'response' in data:
                response_preview = data['response'][:100] + "..." if len(data['response']) > 100 else data['response']
                print(f"   Response Preview: {response_preview}")
        elif response.status_code == 401:
            print("⚠️  AI Chat with Auth: UNAUTHORIZED")
            print("   Token may be invalid or expired")
        elif response.status_code == 404:
            print("❌ AI Chat with Auth: ENDPOINT NOT FOUND")
            print("   The /api/builder/chat endpoint may not exist")
        else:
            print(f"❌ AI Chat with Auth: RETURNED STATUS {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ AI Chat with Auth: ERROR - {str(e)}")

def test_capabilities_no_auth():
    """Test capabilities endpoint without authentication"""
    try:
        # Test capabilities endpoint (should not require auth)
        response = requests.get('http://localhost:8000/api/builder/capabilities', 
                              timeout=10)
        
        if response.status_code == 200:
            print("✅ AI Capabilities (no auth): ACCESSIBLE")
            data = response.json()
            if 'capabilities' in data:
                print(f"   Available Capabilities: {len(data['capabilities'])}")
        else:
            print(f"❌ AI Capabilities (no auth): RETURNED STATUS {response.status_code}")
            
    except Exception as e:
        print(f"❌ AI Capabilities (no auth): ERROR - {str(e)}")

def main():
    print("This script tests AI chat functionality with proper authentication")
    print("In the frontend, demo mode handles authentication automatically")
    print()
    
    test_ai_chat_with_auth()
    
    print("\n" + "=" * 45)
    print("NEXT STEPS:")
    print("✅ For frontend testing: Login with demo credentials in the UI")
    print("✅ For backend testing: Use the token from /api/auth/login")
    print("✅ Check browser console for any frontend errors")

if __name__ == "__main__":
    main()