import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("OPENAI_API_KEY not found in environment variables")
    exit(1)

print("Debugging OpenAI API connection...")

# Test with a simple request to gpt-4o
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-4o",
    "messages": [
        {"role": "user", "content": "Hello, how are you?"}
    ],
    "max_tokens": 100
}

try:
    print("Making request to OpenAI API...")
    response = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=30.0
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        result = response.json()
        print("Success! Response:")
        print(result)
    else:
        print(f"Error Response: {response.text}")
        
except Exception as e:
    print(f"Exception occurred: {e}")
    import traceback
    traceback.print_exc()