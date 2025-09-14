import asyncio
import httpx
from dotenv import load_dotenv
import os

async def test_authenticated_ai_chat():
    """Test the AI chat endpoint with proper authentication."""
    print("🚀 Testing authenticated AI chat...")
    
    # Load environment variables
    load_dotenv()
    
    # Base URL for the backend
    base_url = "http://localhost:8000/api"
    print(f"📍 Base URL: {base_url}")
    
    # Test user credentials (from the /test-user endpoint)
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    print(f"🔐 Login data: {login_data}")
    
    async with httpx.AsyncClient() as client:
        # 1. Login to get access token
        print("\n1. Logging in...")
        try:
            login_response = await client.post(
                f"{base_url}/auth/login",
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            print(f"   Login Status: {login_response.status_code}")
            
            if login_response.status_code != 200:
                print(f"   ❌ Login failed: {login_response.text}")
                return
                
            login_result = login_response.json()
            access_token = login_result.get("access_token")
            print(f"   ✅ Login successful! Token: {access_token[:20]}...")
            
        except Exception as e:
            print(f"   ❌ Request failed with exception: {str(e)}")
            return
        
        # 2. Test AI chat endpoint with the access token
        print("\n2. Testing AI chat...")
        chat_data = {
            "message": "Hello, how can you help me today?"
        }
        
        try:
            chat_response = await client.post(
                f"{base_url}/ai/chat",
                json=chat_data,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            print(f"   Chat Status: {chat_response.status_code}")
            
            if chat_response.status_code == 200:
                chat_result = chat_response.json()
                print(f"   ✅ AI chat successful!")
                print(f"   Response: {chat_result}")
            else:
                print(f"   ❌ AI chat failed: {chat_response.text}")
                
        except Exception as e:
            print(f"   ❌ Chat request failed with exception: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_authenticated_ai_chat())