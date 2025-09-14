import asyncio
import httpx
import traceback

async def test_detailed_chat():
    """Test the AI chat endpoint with detailed error reporting."""
    print("🚀 Testing detailed AI chat...")
    
    base_url = "http://localhost:8000/api"
    print(f"📍 Base URL: {base_url}")
    
    # Test user credentials
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
            print(f"   ❌ Login request failed with exception: {str(e)}")
            traceback.print_exc()
            return
        
        # 2. Test AI chat endpoint with the access token
        print("\n2. Testing AI chat...")
        chat_data = {
            "message": "Hello, how can you help me today?"
        }
        
        try:
            print(f"   Sending chat request to: {base_url}/ai/chat")
            print(f"   Chat data: {chat_data}")
            print(f"   Authorization header: Bearer {access_token[:10]}...")
            
            # Add a timeout to the client request
            chat_response = await client.post(
                f"{base_url}/ai/chat",
                json=chat_data,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=60.0  # Increase timeout to 60 seconds
            )
            print(f"   Chat Status: {chat_response.status_code}")
            
            if chat_response.status_code == 200:
                chat_result = chat_response.json()
                print(f"   ✅ AI chat successful!")
                print(f"   Response: {chat_result}")
            else:
                print(f"   ❌ AI chat failed with status {chat_response.status_code}")
                print(f"   Response: {chat_response.text}")
                
        except httpx.TimeoutException as e:
            print(f"   ❌ Chat request timed out: {str(e)}")
            print("   This might be because the AI service is taking too long to respond.")
            print("   The application should return a fallback response in this case.")
        except Exception as e:
            print(f"   ❌ Chat request failed with exception: {str(e)}")
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_detailed_chat())