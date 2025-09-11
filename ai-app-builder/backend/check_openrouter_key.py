#!/usr/bin/env python3
"""
Script to check OpenRouter API key validity and account status
"""
import httpx
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_openrouter_key():
    """Check OpenRouter API key validity"""
    print("🔍 Checking OpenRouter API key...")
    
    try:
        from app.core.config import settings
        
        if not settings.OPENROUTER_API_KEY:
            print("❌ OpenRouter API key not found in settings")
            return False
            
        print(f"✅ OpenRouter API key found: {'*' * 10}{settings.OPENROUTER_API_KEY[-5:]}")
        
        # Check if the key format is correct
        if not settings.OPENROUTER_API_KEY.startswith("sk-or-"):
            print("⚠️ Warning: API key format doesn't match expected OpenRouter format")
            print("   Expected format: sk-or-...")
            
        # Test API key with a simple request to check account status
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "AI App Builder"
        }
        
        # Test with a minimal request to check key validity
        test_data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": "test"}
            ],
            "max_tokens": 10
        }
        
        print("📤 Testing API key with OpenRouter...")
        
        try:
            response = httpx.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=test_data,
                timeout=30.0
            )
            
            print(f"📡 HTTP Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ API key is valid and working")
                return True
            elif response.status_code == 401:
                print("❌ API key is invalid (401 Unauthorized)")
                print("   Please check your OpenRouter API key in the .env file")
                return False
            elif response.status_code == 402:
                print("❌ API key is valid but account has insufficient balance (402 Payment Required)")
                print("   Please check your OpenRouter account balance and billing information")
                return False
            elif response.status_code == 429:
                print("⚠️ API key is valid but rate limited (429 Too Many Requests)")
                print("   Please wait and try again later")
                return True  # Key is valid, just rate limited
            else:
                print(f"❌ Unexpected response: {response.status_code}")
                print(f"   Response: {response.text}")
                # Check if it's a JSON response with error details
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        print(f"   Error: {error_data['error']}")
                except:
                    pass
                return False
                
        except httpx.RequestError as e:
            print(f"❌ Network error: {e}")
            print("   Please check your internet connection")
            return False
            
    except Exception as e:
        print(f"❌ Error checking OpenRouter key: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 AI App Builder - OpenRouter API Key Check")
    print("=" * 50)
    
    success = check_openrouter_key()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 OpenRouter API key check completed successfully!")
    else:
        print("❌ OpenRouter API key check failed.")
        print("\n🔧 Troubleshooting steps:")
        print("1. Verify your OpenRouter API key in the .env file")
        print("2. Check your internet connection")
        print("3. Visit https://openrouter.ai/ to check your account status")
        print("4. Ensure your API key has sufficient quota/balance")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)