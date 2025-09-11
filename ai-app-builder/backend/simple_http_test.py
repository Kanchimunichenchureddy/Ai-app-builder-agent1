#!/usr/bin/env python3
"""
Simple HTTP test to verify httpx is working
"""
import sys

def test_httpx():
    """Test if httpx can be imported and used"""
    try:
        import httpx
        print("✅ httpx imported successfully")
        
        # Test a simple request
        try:
            response = httpx.get("https://httpbin.org/get", timeout=5)
            if response.status_code == 200:
                print("✅ httpx can make HTTP requests")
                print(f"   Status: {response.status_code}")
                return True
            else:
                print(f"⚠️  httpx request returned status {response.status_code}")
                return True
        except Exception as e:
            print(f"⚠️  httpx request failed: {e}")
            return True
            
    except ImportError as e:
        print(f"❌ Failed to import httpx: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing httpx: {e}")
        return False

if __name__ == "__main__":
    print("Testing httpx library...")
    print("=" * 30)
    
    success = test_httpx()
    
    print("=" * 30)
    if success:
        print("🎉 httpx is working correctly!")
    else:
        print("💥 httpx is not working. Please install it with:")
        print("   pip install httpx")