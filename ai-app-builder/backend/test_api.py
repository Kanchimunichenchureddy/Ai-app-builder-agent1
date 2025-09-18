import requests
import json

# First, let's create a test user
test_user_url = "http://localhost:8001/api/auth/test-user"

try:
    # Create test user
    test_user_response = requests.post(test_user_url)
    print(f"Test User Status Code: {test_user_response.status_code}")
    print(f"Test User Response: {test_user_response.json()}")
    
    # Now authenticate using form data
    login_url = "http://localhost:8001/api/auth/login"
    login_data = {
        "username": "test@example.com",  # Can be email or username
        "password": "testpassword123"
    }
    
    # Use data parameter for form-encoded data
    login_response = requests.post(login_url, data=login_data)
    print(f"Login Status Code: {login_response.status_code}")
    
    if login_response.status_code == 200:
        login_result = login_response.json()
        print(f"Login Response: {login_result}")
        
        # Extract the access token
        access_token = login_result.get("access_token")
        
        if access_token:
            # Now test the chat endpoint with the token
            chat_url = "http://localhost:8001/api/ai/chat"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            chat_data = {
                "message": "Hello, how are you?",
                "context": {}
            }
            
            chat_response = requests.post(chat_url, headers=headers, json=chat_data)
            print(f"Chat Status Code: {chat_response.status_code}")
            print(f"Chat Response: {chat_response.json()}")
        else:
            print("No access token in login response")
    else:
        print(f"Login failed: {login_response.json()}")
        
except Exception as e:
    print(f"Error: {e}")