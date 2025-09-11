#!/usr/bin/env python3
"""
Test script to verify that the AI service is working correctly
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.integrations.openrouter_service import OpenRouterService

async def test_openrouter_service():
    """Test the OpenRouter service"""
    print("Testing OpenRouter Service...")
    
    try:
        # Initialize the service
        service = OpenRouterService()
        
        # Check if API key is configured
        if not service.api_key:
            print("❌ ERROR: OpenRouter API key not found!")
            print("Please check your backend/.env file")
            return False
            
        print(f"✅ API Key found: {service.api_key[:10]}...")
        print(f"✅ Using model: {service.default_model}")
        
        # Test generating a response
        print("\nTesting response generation...")
        system_prompt = "You are a helpful assistant."
        user_prompt = "What is the capital of France?"
        
        response = await service.generate_response(system_prompt, user_prompt)
        
        if response and not response.startswith("{"):
            print("✅ Response generated successfully!")
            print(f"Response: {response}")
            return True
        else:
            print("❌ Failed to generate proper response")
            print(f"Response received: {response}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

async def main():
    print("AI Service Test Script")
    print("=" * 30)
    
    success = await test_openrouter_service()
    
    if success:
        print("\n🎉 All tests passed! The AI service is working correctly.")
    else:
        print("\n💥 Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())