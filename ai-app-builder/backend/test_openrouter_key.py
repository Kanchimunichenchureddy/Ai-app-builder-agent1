#!/usr/bin/env python3
"""
Script to test OpenRouter API key configuration
"""

import os
import sys
import importlib.util

# Add the current directory to the path so we can import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def load_env_file():
    """Load environment variables from .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_path):
        print("❌ .env file not found!")
        return False
    
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✅ .env file loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error loading .env file: {str(e)}")
        return False

def check_openrouter_key():
    """Check if OpenRouter API key is configured"""
    # Try to load from environment
    api_key = os.environ.get('OPENROUTER_API_KEY')
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        return False
    
    if api_key.startswith('sk-or-'):
        print("✅ OpenRouter API Key: PRESENT (format looks correct)")
        # Show first and last few characters for verification (but not the full key)
        if len(api_key) > 20:
            print(f"   Key Preview: {api_key[:10]}...{api_key[-4:]}")
        else:
            print("   Key Preview: [TOO SHORT TO DISPLAY]")
        return True
    else:
        print("⚠️  OPENROUTER_API_KEY found but format may be incorrect")
        print("   Expected format: sk-or-...")
        return False

def test_openrouter_service():
    """Test the OpenRouter service directly"""
    try:
        # Try to import the OpenRouter service
        spec = importlib.util.spec_from_file_location(
            "openrouter_service", 
            os.path.join(os.path.dirname(__file__), "app", "services", "integrations", "openrouter_service.py")
        )
        openrouter_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(openrouter_module)
        
        # Create an instance of the service
        OpenRouterService = getattr(openrouter_module, "OpenRouterService")
        service = OpenRouterService()
        
        print("✅ OpenRouter Service: LOADED SUCCESSFULLY")
        print(f"   API Key Configured: {'YES' if service.api_key else 'NO'}")
        print(f"   Default Model: {service.default_model}")
        
        if service.api_key:
            print("✅ OpenRouter Service is ready for use!")
            return True
        else:
            print("❌ OpenRouter Service loaded but API key is missing")
            return False
            
    except FileNotFoundError:
        print("❌ OpenRouter service file not found!")
        print("   Expected location: app/services/integrations/openrouter_service.py")
        return False
    except Exception as e:
        print(f"❌ Error testing OpenRouter service: {str(e)}")
        return False

def main():
    print("AI App Builder - OpenRouter API Key Test")
    print("=" * 40)
    
    print("\n1. Loading .env file...")
    env_loaded = load_env_file()
    
    if env_loaded:
        print("\n2. Checking OpenRouter API Key...")
        key_ok = check_openrouter_key()
        
        if key_ok:
            print("\n3. Testing OpenRouter Service...")
            test_openrouter_service()
        else:
            print("\n❌ OpenRouter API Key test failed!")
            print("   Please check your backend/.env file and ensure OPENROUTER_API_KEY is properly configured")
    else:
        print("\n❌ Could not load .env file!")
        print("   Please make sure backend/.env file exists and is properly formatted")

if __name__ == "__main__":
    main()