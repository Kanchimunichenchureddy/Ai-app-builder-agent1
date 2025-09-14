import os
import sys
import asyncio
import httpx

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.core.config import settings
except ImportError as e:
    print(f"Failed to import settings: {e}")
    sys.exit(1)

async def test_openrouter_api_detailed():
    """Test OpenRouter API connection with detailed debugging."""
    print("✅ OpenRouter API key configured (length: {})".format(
        len(settings.OPENROUTER_API_KEY) if settings.OPENROUTER_API_KEY else "None"
    ))
    
    if not settings.OPENROUTER_API_KEY:
        print("❌ No API key found")
        return
    
    print("📡 Testing OpenRouter API connection...")
    
    # Using the main domain instead of api subdomain
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "AI App Builder Test"
    }
    
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": "Hello, are you working?"}
        ],
        "max_tokens": 100
    }
    
    print(f"🔍 Request URL: {url}")
    print(f"🔍 Request Headers: {headers}")
    print(f"🔍 Request Data: {data}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                json=data,
                timeout=30.0
            )
            print(f"📊 Response Status: {response.status_code}")
            print(f"📊 Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ API Connection Successful!")
                print("💬 Response:", result["choices"][0]["message"]["content"])
            else:
                print(f"❌ API Connection Failed with status {response.status_code}")
                print("📄 Response Text:", response.text)
                response.raise_for_status()
                
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"📊 Status Code: {e.response.status_code}")
        print(f"📄 Response Text: {e.response.text}")
    except Exception as e:
        print(f"❌ API Connection Failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_openrouter_api_detailed())