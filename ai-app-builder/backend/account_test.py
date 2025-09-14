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

def test_account_info():
    """Test getting account information from OpenRouter."""
    print("✅ OpenRouter API key configured (length: {})".format(
        len(settings.OPENROUTER_API_KEY) if settings.OPENROUTER_API_KEY else "None"
    ))
    
    if not settings.OPENROUTER_API_KEY:
        print("❌ No API key found")
        return
    
    print("📡 Testing OpenRouter account info endpoint...")
    
    # Try the account info endpoint
    url = "https://openrouter.ai/api/v1/auth/key"
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    print(f"🔍 Request URL: {url}")
    print(f"🔍 Request Headers: {headers}")
    
    try:
        response = httpx.get(
            url,
            headers=headers,
            timeout=30.0
        )
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Account info retrieved successfully!")
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
    test_account_info()