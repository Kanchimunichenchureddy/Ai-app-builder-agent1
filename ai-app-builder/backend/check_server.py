#!/usr/bin/env python3
"""
Simple script to check if the backend server is running
"""
import httpx
import asyncio

async def check_server():
    """Check if the backend server is running"""
    print("🔍 Checking if backend server is running...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000", timeout=10.0)
            
        if response.status_code == 200:
            print("✅ Server is running!")
            data = response.json()
            print(f"📝 App Name: {data.get('message', 'N/A')}")
            print(f"🔢 Version: {data.get('version', 'N/A')}")
            print(f"📊 Status: {data.get('status', 'N/A')}")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
            
    except httpx.ConnectError:
        print("❌ Could not connect to server at http://localhost:8000")
        print("   Make sure the backend server is running")
        print("   Start it with: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False

async def check_docs():
    """Check if the API documentation is accessible"""
    print("\n🔍 Checking API documentation...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/docs", timeout=10.0)
            
        if response.status_code == 200:
            print("✅ API documentation is accessible at http://localhost:8000/docs")
            return True
        else:
            print(f"❌ Documentation returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking documentation: {e}")
        return False

async def main():
    print("🚀 AI App Builder - Server Check")
    print("=" * 40)
    
    server_ok = await check_server()
    docs_ok = await check_docs()
    
    print("\n" + "=" * 40)
    if server_ok and docs_ok:
        print("🎉 All checks passed! The server is running correctly.")
        print("\nAccess the application at:")
        print("  Frontend: http://localhost:3000")
        print("  Backend API: http://localhost:8000")
        print("  API Docs: http://localhost:8000/docs")
    else:
        print("❌ Some checks failed.")
        if not server_ok:
            print("\n🔧 To start the backend server:")
            print("   1. Open a terminal in the backend directory")
            print("   2. Run: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
            print("   3. Or run: start_server.bat")
            print("   4. Or run: .\\start_server.ps1")

if __name__ == "__main__":
    asyncio.run(main())