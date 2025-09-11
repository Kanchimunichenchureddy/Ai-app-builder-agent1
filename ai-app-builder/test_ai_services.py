import os
import sys
import asyncio
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

try:
    # Import the configuration
    from app.core.config import settings
    
    print("=== AI Service Configuration Check ===")
    print(f"OPENAI_API_KEY configured: {'Yes' if settings.OPENAI_API_KEY else 'No'}")
    print(f"GEMINI_API_KEY configured: {'Yes' if settings.GEMINI_API_KEY else 'No'}")
    print(f"DEEPSEEK_API_KEY configured: {'Yes' if settings.DEEPSEEK_API_KEY else 'No'}")
    
    # Check if any API keys are configured
    if not any([settings.OPENAI_API_KEY, settings.GEMINI_API_KEY, settings.DEEPSEEK_API_KEY]):
        print("\n❌ No AI service API keys found!")
        print("Please configure at least one AI service in your .env file:")
        print("  OPENAI_API_KEY=your_openai_key")
        print("  GEMINI_API_KEY=your_gemini_key")
        print("  DEEPSEEK_API_KEY=your_deepseek_key")
    else:
        print("\n✅ At least one AI service is configured")
        
        # Test importing AI services
        try:
            from app.services.ai_agent import AIAgentService
            print("✅ AI Agent Service imported successfully")
            
            # Test creating AI agent
            ai_agent = AIAgentService()
            print(f"✅ AI Agent created with active service: {ai_agent.active_llm_service}")
            
            # Test a simple chat
            print("\n=== Testing AI Chat ===")
            
            async def test_chat():
                try:
                    response = await ai_agent.chat_with_user("Hello, this is a test message")
                    print("✅ AI Chat test successful")
                    print(f"Response: {response[:100]}...")
                except Exception as e:
                    print(f"❌ AI Chat test failed: {e}")
            
            # Run the async test
            asyncio.run(test_chat())
            
        except Exception as e:
            print(f"❌ Failed to import or create AI Agent: {e}")
            import traceback
            traceback.print_exc()

except Exception as e:
    print(f"❌ Failed to import configuration: {e}")
    print("Make sure you're running this script from the ai-app-builder directory")
    import traceback
    traceback.print_exc()