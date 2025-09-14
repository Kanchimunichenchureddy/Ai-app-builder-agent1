import os
import sys
import httpx

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.core.config import settings
except ImportError as e:
    print(f"Failed to import settings: {e}")
    sys.exit(1)

def test_api_key_simple():
    """Test OpenRouter API key with a simple synchronous request."""
    print("✅ OpenRouter API key configured (length: {})".format(
        len(settings.OPENROUTER_API_KEY) if settings.OPENROUTER_API_KEY else "None"
    ))
    
    if not settings.OPENROUTER_API_KEY:
        print("❌ No API key found")
        return
    
    print("📡 Testing OpenRouter API connection with simple request...")
    
    # Using the main domain
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Minimal test data
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": "test"}
        ],
        "max_tokens": 10
    }
    
    print(f"🔍 Request URL: {url}")
    print(f"🔍 Request Headers: {headers}")
    print(f"🔍 Request Data: {data}")
    
    try:
        response = httpx.post(
            url,
            headers=headers,
            json=data,
            timeout=30.0
        )
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ API key is valid!")
        elif response.status_code == 401:
            print("❌ API key is invalid (401 Unauthorized)")
        elif response.status_code == 403:
            print("❌ Access forbidden (403)")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_key_simple()