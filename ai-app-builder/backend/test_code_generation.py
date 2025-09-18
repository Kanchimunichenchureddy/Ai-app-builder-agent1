import requests
import json

# First, let's authenticate
login_url = "http://localhost:8001/api/auth/login"
login_data = {
    "username": "test@example.com",
    "password": "testpassword123"
}

try:
    # Authenticate
    login_response = requests.post(login_url, data=login_data)
    
    if login_response.status_code == 200:
        access_token = login_response.json().get("access_token")
        
        if access_token:
            # Test code generation
            code_url = "http://localhost:8001/api/ai/chat"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            code_data = {
                "message": "Write a Python function to calculate the factorial of a number",
                "context": {}
            }
            
            code_response = requests.post(code_url, headers=headers, json=code_data)
            print(f"Code Generation Status Code: {code_response.status_code}")
            
            if code_response.status_code == 200:
                result = code_response.json()
                print(f"Code Generation Response: {result}")
                print(f"Generated Response:\n{result.get('response', 'No response')}")
            else:
                print(f"Code generation failed: {code_response.json()}")
        else:
            print("No access token received")
    else:
        print(f"Authentication failed: {login_response.json()}")
        
except Exception as e:
    print(f"Error: {e}")