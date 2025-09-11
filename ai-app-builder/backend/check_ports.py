import socket
import sys
import time
import requests
from threading import Thread

def check_port(host, port):
    """Check if a port is open on a given host"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def check_http_service(url):
    """Check if an HTTP service is responding"""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code
    except:
        return None

def main():
    print("AI App Builder - Port and Service Checker")
    print("=========================================")
    
    # Check if backend port is open
    print("Checking if backend port (8000) is open...")
    backend_port_open = check_port('localhost', 8000)
    if backend_port_open:
        print("✅ Port 8000 is open")
    else:
        print("❌ Port 8000 is closed")
    
    # Check if frontend port is open
    print("\nChecking if frontend port (3000) is open...")
    frontend_port_open = check_port('localhost', 3000)
    if frontend_port_open:
        print("✅ Port 3000 is open")
    else:
        print("❌ Port 3000 is closed")
    
    # Check if backend service is responding
    print("\nChecking if backend service is responding...")
    backend_status = check_http_service('http://localhost:8000')
    if backend_status:
        print(f"✅ Backend service is responding with status code: {backend_status}")
        # Try to get root endpoint info
        try:
            response = requests.get('http://localhost:8000', timeout=5)
            data = response.json()
            print(f"   Message: {data.get('message', 'N/A')}")
            print(f"   Version: {data.get('version', 'N/A')}")
        except:
            print("   Could not parse response data")
    else:
        print("❌ Backend service is not responding")
    
    # Check if frontend service is responding
    print("\nChecking if frontend service is responding...")
    frontend_status = check_http_service('http://localhost:3000')
    if frontend_status:
        print(f"✅ Frontend service is responding with status code: {frontend_status}")
    else:
        print("❌ Frontend service is not responding")
    
    print("\n=========================================")
    if backend_port_open and backend_status:
        print("✅ Backend is running properly!")
        print("   Access it at: http://localhost:8000")
        print("   API Docs at: http://localhost:8000/docs")
    else:
        print("❌ Backend is not running properly")
        print("   Please start the backend server with:")
        print("   cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    
    if frontend_port_open and frontend_status:
        print("\n✅ Frontend is running properly!")
        print("   Access it at: http://localhost:3000")
    else:
        print("\n❌ Frontend is not running properly")
        print("   Please start the frontend server with:")
        print("   cd frontend && npm start")
    
    print("\n💡 Remember: Use http://localhost:8000 in your browser, NOT 0.0.0.0")

if __name__ == "__main__":
    main()