#!/usr/bin/env python3
"""
Test script to verify AI service updates
"""
import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.ai_agent import AIAgentService

async def test_ai_services():
    print("Testing updated AI services...")
    
    # Initialize AI agent
    ai_agent = AIAgentService()
    print(f"AI agent initialized with LLM service: {ai_agent.active_llm_service}")
    print(f"Model preferences: {ai_agent.model_preferences}")
    
    # Test chat functionality
    print("\nTesting chat functionality...")
    try:
        response = await ai_agent.chat_with_user("Hello, how are you?")
        print(f"Chat response: {response}")
    except Exception as e:
        print(f"Chat test failed: {e}")
    
    # Test code generation
    print("\nTesting code generation...")
    try:
        code_response = await ai_agent.generate_code_from_description("Create a simple React component that displays 'Hello World'")
        print(f"Code generation response: {code_response}")
    except Exception as e:
        print(f"Code generation test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai_services())