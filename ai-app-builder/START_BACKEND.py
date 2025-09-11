#!/usr/bin/env python3
"""
Script to start the backend server automatically
"""

import subprocess
import sys
import os
import time

def start_backend_server():
    """Start the backend server"""
    print("AI App Builder - Backend Server Starter")
    print("=" * 40)
    
    # Check if we're in the right directory
    backend_path = os.path.join(os.getcwd(), "backend")
    
    if not os.path.exists(backend_path):
        print("❌ Backend directory not found!")
        print(f"   Expected at: {backend_path}")
        return False
    
    print("✅ Backend directory found")
    
    # Change to backend directory
    os.chdir(backend_path)
    print("📁 Changed to backend directory")
    
    # Check if requirements are installed
    try:
        import fastapi
        import uvicorn
        print("✅ Required Python packages found")
    except ImportError as e:
        print("❌ Required Python packages missing:")
        print(f"   {str(e)}")
        print("   Please run: pip install -r requirements.txt")
        return False
    
    # Start the backend server
    print("\n🚀 Starting backend server...")
    print("   Command: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    print("   Please wait for startup completion message...")
    print("   Press Ctrl+C to stop the server")
    print("\n" + "=" * 50)
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
        return True
    except KeyboardInterrupt:
        print("\n\n⚠️  Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Failed to start backend server: {str(e)}")
        return False

def main():
    try:
        success = start_backend_server()
        if success:
            print("\n✅ Backend server process completed")
        else:
            print("\n❌ Backend server failed to start")
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")

if __name__ == "__main__":
    main()