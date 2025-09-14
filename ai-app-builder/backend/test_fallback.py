import os
import sys
import asyncio

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.services.ai_agent import AIAgentService
except ImportError as e:
    print(f"Failed to import AIAgentService: {e}")
    sys.exit(1)

async def test_fallback_mechanism():
    """Test the fallback mechanism when OpenRouter is not available."""
    print("🚀 Testing AI Agent fallback mechanism...")
    
    # Create an instance of the AI agent
    ai_agent = AIAgentService()
    
    # Simulate API key not working
    ai_agent.openrouter_api_working = False
    
    # Test chat functionality
    print("\n💬 Testing chat with user...")
    try:
        response = await ai_agent.chat_with_user("Hello, how can you help me?")
        print("✅ Chat response received:")
        print(response[:200] + "..." if len(response) > 200 else response)
    except Exception as e:
        print(f"❌ Chat failed with error: {e}")
    
    # Test code generation
    print("\n💻 Testing code generation...")
    try:
        code_response = await ai_agent.generate_code_from_description("Create a simple React component that displays 'Hello World'")
        print("✅ Code generation response received:")
        print(code_response[:200] + "..." if len(code_response) > 200 else code_response)
    except Exception as e:
        print(f"❌ Code generation failed with error: {e}")

if __name__ == "__main__":
    asyncio.run(test_fallback_mechanism())