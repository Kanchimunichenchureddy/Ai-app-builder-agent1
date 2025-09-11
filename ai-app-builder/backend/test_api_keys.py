import os
import asyncio
import httpx

# Load environment variables from .env file
def load_env_file():
    env_file_path = '.env'
    if os.path.exists(env_file_path):
        with open(env_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value.strip('"').strip("'")
        print("✅ .env file loaded successfully")
    else:
        print("❌ .env file not found")

# Test OpenAI API key
async def test_openai_key():
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello, this is a test."}],
        "max_tokens": 10
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=10.0
            )
            
            if response.status_code == 200:
                print("✅ OpenAI API key is valid")
                return True
            elif response.status_code == 401:
                print("❌ OpenAI API key is invalid or expired")
                return False
            elif response.status_code == 429:
                print("⚠️ OpenAI API key is valid but rate limited")
                return True
            else:
                print(f"❌ OpenAI API error: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"❌ OpenAI connection error: {e}")
        return False

# Test DeepSeek API key
async def test_deepseek_key():
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    if not api_key:
        print("❌ DEEPSEEK_API_KEY not found in environment variables")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "Hello, this is a test."}],
        "max_tokens": 10
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=10.0
            )
            
            if response.status_code == 200:
                print("✅ DeepSeek API key is valid")
                return True
            elif response.status_code == 401:
                print("❌ DeepSeek API key is invalid or expired")
                return False
            elif response.status_code == 429:
                print("⚠️ DeepSeek API key is valid but rate limited")
                return True
            else:
                print(f"❌ DeepSeek API error: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"❌ DeepSeek connection error: {e}")
        return False

# Test Gemini API key
async def test_gemini_key():
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        return False
    
    data = {
        "contents": [{
            "parts": [{
                "text": "Hello, this is a test."
            }]
        }]
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={api_key}",
                json=data,
                timeout=10.0
            )
            
            if response.status_code == 200:
                print("✅ Gemini API key is valid")
                return True
            elif response.status_code == 401:
                print("❌ Gemini API key is invalid or expired")
                return False
            elif response.status_code == 429:
                print("⚠️ Gemini API key is valid but rate limited")
                return True
            else:
                print(f"❌ Gemini API error: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"❌ Gemini connection error: {e}")
        return False

async def main():
    print("=== AI Service API Key Tester ===")
    
    # Load environment variables
    load_env_file()
    
    print("\n=== Testing API Keys ===")
    
    # Test each service
    await test_openai_key()
    await test_deepseek_key()
    await test_gemini_key()
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    asyncio.run(main())