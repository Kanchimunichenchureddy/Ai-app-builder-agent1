#!/usr/bin/env python3
"""
Test script to verify OpenRouter service connectivity
"""
import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_openrouter_service():
    """Test OpenRouter service connectivity"""
    print("🔍 Testing OpenRouter service connectivity...")
    
    try:
        # Import the OpenRouter service
        from app.services.integrations.openrouter_service import OpenRouterService
        from app.core.config import settings
        
        # Check if API key is configured
        if not settings.OPENROUTER_API_KEY:
            print("❌ OpenRouter API key not found in settings")
            return False
            
        print(f"✅ OpenRouter API key found: {'*' * 10}{settings.OPENROUTER_API_KEY[-5:]}")
        
        # Initialize the service
        service = OpenRouterService()
        print("✅ OpenRouter service initialized")
        
        # Test a simple request
        print("📤 Sending test request to OpenRouter...")
        response = await service.generate_response(
            "You are a helpful assistant.", 
            "Hello, this is a test message. Please respond with 'Test successful' if you receive this."
        )
        
        if response and not response.startswith("// Fallback"):
            print("✅ OpenRouter service is working correctly")
            print(f"📝 Response: {response[:100]}{'...' if len(response) > 100 else ''}")
            return True
        else:
            print("❌ OpenRouter service returned fallback response")
            print(f"📝 Response: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing OpenRouter service: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_ai_agent():
    """Test AI Agent service"""
    print("\n🤖 Testing AI Agent service...")
    
    try:
        from app.services.ai_agent import AIAgentService
        
        # Initialize the AI agent
        ai_agent = AIAgentService()
        print("✅ AI Agent service initialized")
        
        # Test a simple chat with correct parameters
        print("📤 Sending test message to AI Agent...")
        # Pass context as a dictionary, not a string
        context = {"user_id": "test_user"}
        response = await ai_agent.chat_with_user("Hello, this is a test message.", context)
        
        if response and not response.startswith("// Fallback"):
            print("✅ AI Agent service is working correctly")
            print(f"📝 Response: {response[:100]}{'...' if len(response) > 100 else ''}")
            return True
        else:
            print("❌ AI Agent service returned fallback response")
            print(f"📝 Response: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing AI Agent service: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🚀 AI App Builder - OpenRouter Service Test")
    print("=" * 50)
    
    # Test OpenRouter service
    openrouter_success = await test_openrouter_service()
    
    # Test AI Agent service
    ai_agent_success = await test_ai_agent()
    
    print("\n" + "=" * 50)
    if openrouter_success and ai_agent_success:
        print("🎉 All tests passed! The AI services are working correctly.")
        print("\nYou should now be able to use the AI chat without connection errors.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        
        if not openrouter_success:
            print("\n🔧 Troubleshooting steps for OpenRouter:")
            print("1. Verify your OpenRouter API key in the .env file")
            print("2. Check your internet connection")
            print("3. Verify that the OpenRouter API is accessible")
            print("4. Check if your API key has sufficient quota")
            
        if not ai_agent_success:
            print("\n🔧 Troubleshooting steps for AI Agent:")
            print("1. Check the backend server logs for errors")
            print("2. Verify that all services are properly initialized")
            print("3. Check if there are any import errors in the service files")
    
    return openrouter_success and ai_agent_success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)