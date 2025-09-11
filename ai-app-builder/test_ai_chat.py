#!/usr/bin/env python3
"""
Test script to verify AI chat functionality
"""

import asyncio
import sys
import os

# Add the backend directory to the path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

async def test_ai_chat():
    """Test the AI chat functionality"""
    print("Testing AI Chat Functionality...")
    
    try:
        # Import the AI agent service
        from app.services.ai_agent import AIAgentService
        
        # Initialize the AI agent
        ai_agent = AIAgentService()
        
        print("✅ AI Agent initialized successfully")
        print(f"✅ Using LLM service: {ai_agent.active_llm_service}")
        
        # Test chat functionality
        print("\nTesting chat with AI agent...")
        test_message = "Hello, what can you help me with?"
        context = {"user_id": "test_user"}
        
        response = await ai_agent.chat_with_user(test_message, context)
        
        print("✅ Chat test successful!")
        print(f"Response: {response[:200]}{'...' if len(response) > 200 else ''}")
        
        # Test code generation
        print("\nTesting code generation...")
        code_description = "Create a simple React component that displays 'Hello World'"
        
        code_response = await ai_agent.generate_code_from_description(code_description)
        
        print("✅ Code generation test successful!")
        print(f"Generated code preview: {code_response[:200]}{'...' if len(code_response) > 200 else ''}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("AI Chat Test Script")
    print("=" * 30)
    
    try:
        success = await test_ai_chat()
        
        if success:
            print("\n🎉 All AI chat tests passed!")
            print("The AI chat functionality is working correctly.")
        else:
            print("\n💥 Some tests failed.")
            print("Please check the errors above.")
    except Exception as e:
        print(f"❌ Failed to run tests: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())