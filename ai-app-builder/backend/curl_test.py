import os
import sys
import subprocess

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.core.config import settings
except ImportError as e:
    print(f"Failed to import settings: {e}")
    sys.exit(1)

def test_with_curl():
    """Test OpenRouter API connection using cURL."""
    print("✅ OpenRouter API key configured (length: {})".format(
        len(settings.OPENROUTER_API_KEY) if settings.OPENROUTER_API_KEY else "None"
    ))
    
    if not settings.OPENROUTER_API_KEY:
        print("❌ No API key found")
        return
    
    # Create a cURL command to test the API
    curl_command = [
        "curl",
        "-X", "POST",
        "https://openrouter.ai/api/v1/chat/completions",
        "-H", f"Authorization: Bearer {settings.OPENROUTER_API_KEY}",
        "-H", "Content-Type: application/json",
        "-H", "HTTP-Referer: http://localhost:3000",
        "-H", "X-Title: AI App Builder Test",
        "-d", '{"model": "mistralai/mistral-7b-instruct", "messages": [{"role": "user", "content": "Hello, are you working?"}], "max_tokens": 100}'
    ]
    
    print("📡 Testing OpenRouter API connection with cURL...")
    print("🔍 cURL command:")
    print(" ".join(curl_command))
    
    try:
        # Run the cURL command
        result = subprocess.run(curl_command, capture_output=True, text=True, timeout=30)
        print(f"📊 Return code: {result.returncode}")
        print(f"📄 stdout: {result.stdout}")
        if result.stderr:
            print(f"❌ stderr: {result.stderr}")
    except Exception as e:
        print(f"❌ cURL test failed with exception: {e}")

if __name__ == "__main__":
    test_with_curl()