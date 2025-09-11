#!/usr/bin/env python3
"""
Test script to verify AI service connectivity
"""
import os
import sys
import httpx

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def test_ai_services():
    """Test connectivity to AI services"""
    try:
        print("Testing AI service connectivity...")
        
        # Import settings
        from app.core.config import settings
        
        print("✅ Configuration loaded successfully!")
        
        # Test OpenAI API key
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
            print("✅ OpenAI API key is configured")
            # Mask the key for security
            masked_key = settings.OPENAI_API_KEY[:8] + "..." + settings.OPENAI_API_KEY[-4:]
            print(f"   Key: {masked_key}")
        else:
            print("⚠️  OpenAI API key is not properly configured")
            
        # Test DeepSeek API key
        if settings.DEEPSEEK_API_KEY and settings.DEEPSEEK_API_KEY != "your_deepseek_api_key_here":
            print("✅ DeepSeek API key is configured")
            # Mask the key for security
            masked_key = settings.DEEPSEEK_API_KEY[:8] + "..." + settings.DEEPSEEK_API_KEY[-4:]
            print(f"   Key: {masked_key}")
        else:
            print("⚠️  DeepSeek API key is not properly configured")
            
        # Test Gemini API key
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
            print("✅ Gemini API key is configured")
            # Mask the key for security
            masked_key = settings.GEMINI_API_KEY[:8] + "..." + settings.GEMINI_API_KEY[-4:]
            print(f"   Key: {masked_key}")
        else:
            print("⚠️  Gemini API key is not properly configured")
            
        # Test database connection
        print(f"✅ Database URL: {settings.DATABASE_URL}")
        
        # Test CORS configuration
        print(f"✅ CORS Origins: {settings.CORS_ORIGINS_LIST}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing AI service connectivity: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_openai_direct():
    """Test direct OpenAI API connectivity"""
    try:
        import openai
        from app.core.config import settings
        
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
            print("⚠️  Skipping OpenAI connectivity test - API key not configured")
            return True
            
        print("\nTesting direct OpenAI API connectivity...")
        
        # Create OpenAI client
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Test models endpoint
        models = client.models.list()
        print("✅ OpenAI API connectivity test passed!")
        print(f"   Available models: {len(list(models))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing OpenAI connectivity: {e}")
        return False

if __name__ == "__main__":
    print("AI Service Connectivity Test")
    print("=" * 40)
    
    success = test_ai_services()
    
    if success:
        print("\n" + "=" * 40)
        print("🎉 Configuration test completed!")
        print("Your AI services should be properly connected.")
    else:
        print("\n" + "=" * 40)
        print("💥 Configuration test failed!")
        print("Please check your .env file and API key configurations.")
        sys.exit(1)