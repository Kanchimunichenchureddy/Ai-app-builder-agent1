#!/usr/bin/env python3
"""
Script to check exact versions of installed packages
"""
import sys

def check_package_versions():
    """Check versions of key packages"""
    packages = [
        "pydantic",
        "pydantic_settings",
        "fastapi",
        "uvicorn",
        "openai",
        "httpx",
        "google.generativeai",
        "google.auth"
    ]
    
    print("Checking package versions...")
    print("=" * 40)
    
    for package_import in packages:
        try:
            # Handle special import names
            if package_import == "pydantic_settings":
                import pydantic_settings
                version = getattr(pydantic_settings, '__version__', 'Unknown')
                print(f"✅ {package_import:<20} : {version}")
            elif package_import == "google.generativeai":
                import google.generativeai
                version = getattr(google.generativeai, '__version__', 'Unknown')
                print(f"✅ {package_import:<20} : {version}")
            elif package_import == "google.auth":
                import google.auth
                version = getattr(google.auth, '__version__', 'Unknown')
                print(f"✅ {package_import:<20} : {version}")
            else:
                module = __import__(package_import)
                version = getattr(module, '__version__', 'Unknown')
                print(f"✅ {package_import:<20} : {version}")
        except ImportError as e:
            print(f"❌ {package_import:<20} : NOT INSTALLED ({e})")
        except Exception as e:
            print(f"⚠️  {package_import:<20} : ERROR ({e})")

def check_pydantic_internal():
    """Check if pydantic._internal is available"""
    print("\nChecking Pydantic internal modules...")
    print("=" * 40)
    
    try:
        import pydantic
        print(f"✅ Pydantic version: {pydantic.__version__}")
        
        # Try to import _internal
        try:
            from pydantic import _internal
            print("✅ pydantic._internal is available")
        except ImportError:
            print("❌ pydantic._internal is NOT available")
            
        # Try to import specific modules that might be needed
        try:
            from pydantic import BaseModel
            print("✅ pydantic.BaseModel is available")
        except ImportError as e:
            print(f"❌ pydantic.BaseModel is NOT available: {e}")
            
        try:
            from pydantic_settings import BaseSettings
            print("✅ pydantic_settings.BaseSettings is available")
        except ImportError as e:
            print(f"❌ pydantic_settings.BaseSettings is NOT available: {e}")
            
    except ImportError as e:
        print(f"❌ Pydantic is NOT installed: {e}")

if __name__ == "__main__":
    print("AI App Builder - Package Version Check")
    print("=" * 50)
    
    check_package_versions()
    check_pydantic_internal()
    
    print("\n" + "=" * 50)
    print("💡 If you see version conflicts or missing modules:")
    print("   1. Run: python install_deps.py")
    print("   2. Or manually: pip install -r requirements.txt --force-reinstall")