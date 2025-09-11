import os
import sys
import asyncio
from pathlib import Path

# We're already in the backend directory, so no need to change
# Import the modules directly
try:
    from app.core.config import settings
    from app.services.ai_agent import AIAgentService
    
    print("=== AI Service Configuration Check ===")
    print(f"OPENAI_API_KEY: {'✅ Configured' if settings.OPENAI_API_KEY else '❌ Not configured'}")
    print(f"GEMINI_API_KEY: {'✅ Configured' if settings.GEMINI_API_KEY else '❌ Not configured'}")
    print(f"DEEPSEEK_API_KEY: {'✅ Configured' if settings.DEEPSEEK_API_KEY else '❌ Not configured'}")
    
    if not any([settings.OPENAI_API_KEY, settings.GEMINI_API_KEY, settings.DEEPSEEK_API_KEY]):
        print("\n❌ No AI service API keys found!")
        print("Please configure at least one AI service in your .env file:")
        print("  OPENAI_API_KEY=your_openai_key")
        print("  GEMINI_API_KEY=your_gemini_key")
        print("  DEEPSEEK_API_KEY=your_deepseek_key")
    else:
        print("\n✅ At least one AI service is configured")
        
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
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()