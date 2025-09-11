import requests
import json

# Test the backend chat functionality
def test_chat():
    base_url = "http://localhost:8000/api"
    
    # Test login with demo credentials
    login_data = {
        "username": "demo@appforge.dev",
        "password": "demo123"
    }
    
    # Format as form data
    form_data = {
        "username": login_data["username"],
        "password": login_data["password"]
    }
    
    try:
        print("Testing login...")
        # Try to login
        response = requests.post(
            f"{base_url}/auth/login",
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        print(f"Login Status Code: {response.status_code}")
        print(f"Login Response: {response.json()}")
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            if token:
                print("Login successful!")
                print(f"Token: {token}")
                
                # Test chat endpoint
                print("\nTesting chat endpoint...")
                chat_data = {
                    "message": "Hello, how are you?",
                    "context": {}
                }
                
                chat_response = requests.post(
                    f"{base_url}/builder/chat",
                    json=chat_data,
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                print(f"Chat Status Code: {chat_response.status_code}")
                if chat_response.status_code == 200:
                    print(f"Chat Response: {chat_response.json()}")
                    print("Chat test successful!")
                else:
                    print(f"Chat Error: {chat_response.text}")
            else:
                print("No access token in response")
        else:
            print("Login failed")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chat()