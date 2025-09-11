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

print("Testing OpenAI API key and available models...")

# Test the API key by listing models
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

try:
    response = httpx.get(
        "https://api.openai.com/v1/models",
        headers=headers,
        timeout=30.0
    )
    
    if response.status_code == 200:
        models_data = response.json()
        print(f"API key is valid. Found {len(models_data.get('data', []))} models:")
        
        # Filter for GPT models
        gpt_models = [model for model in models_data.get('data', []) if model['id'].startswith('gpt')]
        
        print("\nAvailable GPT models:")
        for model in gpt_models:
            print(f"  - {model['id']}")
            
        # Check if gpt-4-turbo is available
        gpt4_turbo_available = any(model['id'] == 'gpt-4-turbo' for model in gpt_models)
        print(f"\nIs gpt-4-turbo available: {gpt4_turbo_available}")
        
        # Suggest a fallback model if gpt-4-turbo is not available
        if not gpt4_turbo_available:
            if any(model['id'] == 'gpt-4' for model in gpt_models):
                print("Suggested fallback model: gpt-4")
            elif any(model['id'] == 'gpt-3.5-turbo' for model in gpt_models):
                print("Suggested fallback model: gpt-3.5-turbo")
            else:
                print("No suitable fallback model found")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        
except Exception as e:
    print(f"Error testing OpenAI API: {e}")