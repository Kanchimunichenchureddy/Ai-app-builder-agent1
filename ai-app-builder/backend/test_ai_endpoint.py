import httpx
import asyncio
import json

async def test_ai_chat():
    """Test the AI chat endpoint."""
    url = "http://localhost:8000/api/ai/chat"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "message": "Hello, how can you help me?"
    }
    
    print("🚀 Testing AI chat endpoint...")
    print(f"📍 URL: {url}")
    print(f"📨 Data: {data}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data, timeout=30.0)
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ AI chat endpoint is working!")
                response_data = response.json()
                print(f"💬 AI Response: {response_data.get('response', 'No response field found')}")
            else:
                print(f"❌ AI chat endpoint failed with status {response.status_code}")
                print(f"📄 Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Request failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_ai_chat())