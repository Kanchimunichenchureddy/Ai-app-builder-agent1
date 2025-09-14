import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.core.config import settings
except ImportError as e:
    print(f"Failed to import settings: {e}")
    sys.exit(1)

def inspect_api_key():
    """Inspect the API key for hidden characters or issues."""
    if not settings.OPENROUTER_API_KEY:
        print("❌ No API key found")
        return
    
    api_key = settings.OPENROUTER_API_KEY
    print(f"✅ API Key Length: {len(api_key)}")
    print(f"✅ API Key Type: {type(api_key)}")
    print(f"✅ API Key Starts With: {api_key[:15]}")
    print(f"✅ API Key Ends With: {api_key[-10:]}")
    
    # Check for hidden characters
    print(f"✅ API Key Repr: {repr(api_key)}")
    
    # Check each character
    for i, char in enumerate(api_key):
        if ord(char) < 32 or ord(char) > 126:
            print(f"⚠️  Non-printable character at position {i}: {repr(char)} (ord: {ord(char)})")
    
    # Check for common issues
    if api_key.startswith('"') or api_key.endswith('"'):
        print("⚠️  API Key has quotes around it!")
        
    if api_key.startswith("'") or api_key.endswith("'"):
        print("⚠️  API Key has single quotes around it!")
        
    if " " in api_key:
        print("⚠️  API Key contains spaces!")
        
    if "\n" in api_key or "\r" in api_key:
        print("⚠️  API Key contains line breaks!")
        
    # Try to validate format
    if not api_key.startswith("sk-or-v1-"):
        print("⚠️  API Key doesn't start with expected prefix 'sk-or-v1-'")
    else:
        print("✅ API Key has correct prefix")

if __name__ == "__main__":
    inspect_api_key()