import asyncio
import httpx
import os
from dotenv import load_dotenv

async def test_openrouter_directly():
    """Test OpenRouter API directly."""
    print("🚀 Testing OpenRouter API directly...")
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        return
    
    print(f"✅ OpenRouter API key configured (length: {len(api_key)})")
    
    # Test data
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "AI App Builder"
    }
    
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": "Hello, are you working?"}
        ],
        "max_tokens": 100
    }
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    print(f"📡 Testing OpenRouter API connection...")
    print(f"🔍 Request URL: {url}")
    print(f"🔍 Request Headers: {headers}")
    print(f"🔍 Request Data: {data}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data, timeout=30.0)
            print(f"📊 Response Status: {response.status_code}")
            print(f"📊 Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"✅ API Connection Successful!")
                print(f"📄 Response: {response_data}")
            else:
                print(f"❌ API Connection Failed with status {response.status_code}")
                print(f"📄 Response Text: {response.text}")
                
    except Exception as e:
        print(f"❌ API Connection Failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_openrouter_directly())