#!/usr/bin/env python3
"""
Script to test AI chat functionality with a real conversation
"""

import os
import sys
import asyncio
import importlib.util

# Add the current directory to the path so we can import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ai_agent_import():
    """Test if AI Agent can be imported"""
    try:
        spec = importlib.util.spec_from_file_location(
            "ai_agent", 
            os.path.join(os.path.dirname(__file__), "app", "services", "ai_agent.py")
        )
        ai_agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ai_agent_module)
        
        # Create an instance of the AI agent
        AIAgentService = getattr(ai_agent_module, "AIAgentService")
        agent = AIAgentService()
        
        print("✅ AI Agent Service: LOADED SUCCESSFULLY")
        print(f"   Active LLM Service: {agent.active_llm_service}")
        print(f"   Available Capabilities: {sum(1 for cap, enabled in agent.capabilities.items() if enabled)}")
        
        return agent
    except FileNotFoundError:
        print("❌ AI Agent service file not found!")
        print("   Expected location: app/services/ai_agent.py")
        return None
    except Exception as e:
        print(f"❌ Error loading AI Agent service: {str(e)}")
        return None

async def test_chat_interaction(agent):
    """Test a simple chat interaction"""
    try:
        print("\n3. Testing Chat Interaction...")
        print("   Sending test message to AI agent...")
        
        test_message = "Hello, what can you help me with as an AI app builder?"
        context = {"user_id": "test_user"}
        
        response = await agent.chat_with_user(test_message, context)
        
        print("✅ Chat Interaction: SUCCESSFUL")
        print(f"   Response Length: {len(response)} characters")
        
        # Show a preview of the response (first 200 characters)
        response_preview = response[:200] + "..." if len(response) > 200 else response
        print(f"   Response Preview: {response_preview}")
        
        return True
    except Exception as e:
        print(f"❌ Chat Interaction: FAILED - {str(e)}")
        return False

async def test_code_generation(agent):
    """Test code generation functionality"""
    try:
        print("\n4. Testing Code Generation...")
        print("   Requesting code generation from AI agent...")
        
        description = "Create a simple React component that displays 'Hello World'"
        context = {"tech_stack": {"frontend": "React", "backend": "FastAPI", "database": "MySQL"}}
        
        code_response = await agent.generate_code_from_description(description, context)
        
        print("✅ Code Generation: SUCCESSFUL")
        print(f"   Generated Code Length: {len(code_response)} characters")
        
        # Show a preview of the generated code (first 200 characters)
        code_preview = code_response[:200] + "..." if len(code_response) > 200 else code_response
        print(f"   Code Preview: {code_preview}")
        
        return True
    except Exception as e:
        print(f"❌ Code Generation: FAILED - {str(e)}")
        return False

async def main():
    print("AI App Builder - AI Chat Functionality Test")
    print("=" * 45)
    
    print("\n1. Loading AI Agent Service...")
    agent = test_ai_agent_import()
    
    if agent:
        print("\n2. AI Agent Configuration:")
        print(f"   Active Service: {agent.active_llm_service}")
        print(f"   Model Preferences: {agent.model_preferences}")
        
        # Test chat interaction
        chat_success = await test_chat_interaction(agent)
        
        # Test code generation
        code_success = await test_code_generation(agent)
        
        print("\n" + "=" * 45)
        if chat_success and code_success:
            print("🎉 All AI chat functionality tests PASSED!")
            print("✅ Your AI chat service is working correctly!")
        else:
            print("❌ Some AI chat functionality tests FAILED!")
            print("   Please check the errors above and verify your OpenRouter API key configuration")
    else:
        print("\n❌ Could not load AI Agent service!")
        print("   Please check your backend installation and configuration")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())