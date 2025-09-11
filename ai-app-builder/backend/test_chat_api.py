import requests
import json

# Test the chat endpoint
def test_chat_endpoint():
    """Test the chat endpoint with a simple message."""
    print("Testing chat endpoint...")
    
    # First, let's try to create a test user and get a token
    try:
        # Register a test user
        register_data = {
            "email": "test@example.com",
            "password": "testpassword",
            "username": "testuser",
            "full_name": "Test User"
        }
        
        print("1. Registering test user...")
        # Note: We're using demo credentials which should work without backend
        print("   Using demo credentials for testing...")
        
        # Create a mock token for demo user
        token = "mock-jwt-token-12345"
        
        # Test the chat endpoint
        print("2. Testing chat endpoint...")
        chat_data = {
            "message": "Hello, how are you?",
            "context": {}
        }
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Try to call the chat endpoint
        response = requests.post(
            "http://localhost:8000/api/builder/chat",
            json=chat_data,
            headers=headers
        )
        
        print(f"   Status code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   Chat endpoint test passed!")
            return True
        else:
            print("   Chat endpoint test failed!")
            return False
            
    except Exception as e:
        print(f"Chat endpoint test failed with exception: {e}")
        return False

if __name__ == "__main__":
    print("Running chat API test...")
    
    success = test_chat_endpoint()
    
    if success:
        print("\nChat API test passed!")
    else:
        print("\nChat API test failed!")