import requests
import time

def test_backend_endpoints():
    base_url = "http://localhost:8000"
    
    # Test endpoints to check
    endpoints = [
        ("/", "Root endpoint"),
        ("/docs", "Swagger UI documentation"),
        ("/health", "Health check")
    ]
    
    print("Testing AI App Builder Backend Endpoints")
    print("=" * 50)
    
    for endpoint, description in endpoints:
        url = base_url + endpoint
        try:
            print(f"\nTesting {description}: {url}")
            response = requests.get(url, timeout=5)
            print(f"  Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"  Status: ✅ SUCCESS")
                if endpoint == "/":
                    try:
                        data = response.json()
                        print(f"  Response: {data}")
                    except:
                        print(f"  Response: {response.text[:100]}...")
            else:
                print(f"  Status: ❌ FAILED")
                print(f"  Response: {response.text[:100] if response.text else 'No response body'}")
        except requests.exceptions.ConnectionError:
            print(f"  Status: ❌ CONNECTION FAILED")
            print(f"  Error: Could not connect to server")
        except requests.exceptions.Timeout:
            print(f"  Status: ❌ TIMEOUT")
            print(f"  Error: Request timed out")
        except Exception as e:
            print(f"  Status: ❌ ERROR")
            print(f"  Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Test completed")

if __name__ == "__main__":
    test_backend_endpoints()