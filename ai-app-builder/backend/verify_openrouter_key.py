import asyncio
import httpx
import os
from dotenv import load_dotenv

async def verify_openrouter_key():
    """Verify that the OpenRouter API key is working correctly."""
    print("🔍 Verifying OpenRouter API Key...")
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        print("Please make sure you have set the OPENROUTER_API_KEY in your .env file")
        return False
    
    print(f"✅ OpenRouter API key found (length: {len(api_key)})")
    
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
        "max_tokens": 50
    }
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    print(f"📡 Testing connection to OpenRouter...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data, timeout=30.0)
            
            if response.status_code == 200:
                response_data = response.json()
                print("✅ OpenRouter API key is working correctly!")
                print(f"🤖 AI Response: {response_data['choices'][0]['message']['content']}")
                return True
            elif response.status_code == 401:
                error_text = response.text
                if "User not found" in error_text:
                    print("❌ Invalid API key or account not found")
                    print("Please check your API key at https://openrouter.ai/")
                else:
                    print(f"❌ Unauthorized (401): {error_text}")
                return False
            elif response.status_code == 402:
                print("❌ Payment required - please check your account balance")
                return False
            elif response.status_code == 429:
                print("❌ Rate limit exceeded - please try again later")
                return False
            else:
                print(f"❌ API Error: HTTP {response.status_code}")
                print(f"📄 Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Connection failed with exception: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(verify_openrouter_key())
    if success:
        print("\n🎉 Your OpenRouter API key is ready to use!")
        print("You can now start both frontend and backend servers.")
    else:
        print("\n⚠️  Please follow the setup guide in OPENROUTER_SETUP.md")
        print("   to configure a valid API key.")