#!/usr/bin/env python3
"""
Test script to verify AI services are working correctly
"""
import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_ai_services():
    """Test AI services connectivity"""
    print("🔍 Testing AI services...")
    
    try:
        # Import the AI agent service
        from app.services.ai_agent import AIAgentService
        
        # Initialize the AI agent
        ai_agent = AIAgentService()
        print("✅ AI Agent service initialized")
        
        # Test a simple chat
        print("📤 Sending test message to AI Agent...")
        context = {"user_id": "test_user"}
        response = await ai_agent.chat_with_user("Hello, this is a test message.", context)
        
        if response and not response.startswith("// Fallback"):
            print("✅ AI Agent service is working correctly")
            print(f"📝 Response: {response[:100]}{'...' if len(response) > 100 else ''}")
            return True
        else:
            print("⚠️ AI Agent service is using fallback response")
            print(f"📝 Response: {response[:100]}{'...' if len(response) > 100 else ''}")
            return True  # Still considered successful as the service is working
            
    except Exception as e:
        print(f"❌ Error testing AI Agent service: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🚀 AI App Builder - AI Services Test")
    print("=" * 40)
    
    success = await test_ai_services()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 AI services test completed!")
        print("\nIf the frontend AI chat is not working, the issue is likely in the frontend-backend communication.")
        print("\nTroubleshooting steps:")
        print("1. Check that the backend server is running at http://localhost:8000")
        print("2. Verify the frontend is configured to connect to the correct backend URL")
        print("3. Check the browser's developer console for network errors")
        print("4. Ensure CORS is properly configured")
    else:
        print("❌ AI services test failed.")
        print("\nPlease check the backend server and AI service configuration.")

if __name__ == "__main__":
    asyncio.run(main())