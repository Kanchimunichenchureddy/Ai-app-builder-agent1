import os
import sys
import asyncio
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

print("=== AI Service Configuration Diagnostic ===")

# Load environment variables
env_path = backend_path / ".env"
if env_path.exists():
    print(f"✅ Found .env file at: {env_path}")
    # Manually load .env file
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value.strip('"').strip("'")
else:
    print(f"❌ .env file not found at: {env_path}")

print("\n=== Environment Variables Check ===")
openai_key = os.environ.get('OPENAI_API_KEY', '')
gemini_key = os.environ.get('GEMINI_API_KEY', '')
deepseek_key = os.environ.get('DEEPSEEK_API_KEY', '')

print(f"OPENAI_API_KEY: {'✅ Configured' if openai_key else '❌ Not configured'}")
print(f"GEMINI_API_KEY: {'✅ Configured' if gemini_key else '❌ Not configured'}")
print(f"DEEPSEEK_API_KEY: {'✅ Configured' if deepseek_key else '❌ Not configured'}")

if not any([openai_key, gemini_key, deepseek_key]):
    print("\n❌ No AI service API keys found!")
    print("Please configure at least one AI service in your .env file:")
    print("  OPENAI_API_KEY=your_openai_key")
    print("  GEMINI_API_KEY=your_gemini_key")
    print("  DEEPSEEK_API_KEY=your_deepseek_key")
else:
    print("\n✅ At least one AI service is configured")
    
    # Test importing AI services
    try:
        # Import the configuration
        from app.core.config import settings
        print("✅ Configuration loaded successfully")
        print(f"OPENAI_API_KEY from settings: {'✅ Configured' if settings.OPENAI_API_KEY else '❌ Not configured'}")
        print(f"GEMINI_API_KEY from settings: {'✅ Configured' if settings.GEMINI_API_KEY else '❌ Not configured'}")
        print(f"DEEPSEEK_API_KEY from settings: {'✅ Configured' if settings.DEEPSEEK_API_KEY else '❌ Not configured'}")
        
        from app.services.ai_agent import AIAgentService
        print("✅ AI Agent Service imported successfully")
        
        # Test creating AI agent
        ai_agent = AIAgentService()
        print(f"✅ AI Agent created with active service: {ai_agent.active_llm_service}")
        
        # Test a simple chat
        print("\n=== Testing AI Chat ===")
        
        async def test_chat():
            try:
                response = await ai_agent.chat_with_user("Hello, this is a test message. Please respond with a short greeting.")
                print("✅ AI Chat test successful")
                print(f"Response: {response[:200]}...")
                return True
            except Exception as e:
                print(f"❌ AI Chat test failed: {e}")
                import traceback
                traceback.print_exc()
                return False
        
        # Run the async test
        success = asyncio.run(test_chat())
        
        if success:
            print("\n🎉 All tests passed! The AI chat should work properly.")
        else:
            print("\n⚠️  There might be an issue with the AI service connectivity.")
            print("Please check your API keys and internet connection.")
            
    except Exception as e:
        print(f"❌ Failed to import or create AI Agent: {e}")
        import traceback
        traceback.print_exc()