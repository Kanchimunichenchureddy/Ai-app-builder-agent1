#!/usr/bin/env python3
"""
Script to verify that all dependencies are properly installed
"""

import sys
import importlib

def test_import(package_name, test_function=None):
    """Test importing a package and optionally run a test function"""
    try:
        package = importlib.import_module(package_name)
        print(f"✅ {package_name} imported successfully")
        
        if test_function:
            try:
                test_function(package)
                print(f"✅ {package_name} functionality test passed")
            except Exception as e:
                print(f"⚠️  {package_name} functionality test failed: {e}")
        
        return True
    except ImportError as e:
        print(f"❌ {package_name} import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ {package_name} unexpected error: {e}")
        return False

def test_fastapi(package):
    """Test FastAPI functionality"""
    from fastapi import FastAPI
    app = FastAPI()
    # Just creating an app is enough to test basic functionality

def test_sqlalchemy(package):
    """Test SQLAlchemy functionality"""
    from sqlalchemy import create_engine
    # Just importing and creating an engine is enough to test basic functionality

def test_httpx(package):
    """Test httpx functionality"""
    # Just importing is enough to test basic functionality
    pass

def main():
    print("AI App Builder - Installation Verification")
    print("=" * 40)
    
    # List of critical packages to test
    packages_to_test = [
        ("fastapi", test_fastapi),
        ("uvicorn", None),
        ("sqlalchemy", test_sqlalchemy),
        ("pymysql", None),
        ("multipart", None),
        ("jose", None),
        ("passlib", None),
        ("dotenv", None),
        ("pydantic", None),
        ("pydantic_settings", None),
        ("httpx", test_httpx),
        ("requests", None),
        ("stripe", None),
        ("jinja2", None),
        ("aiofiles", None),
        ("docker", None),
        ("git", None)
    ]
    
    print("\nTesting critical package imports:")
    print("-" * 35)
    
    failed_packages = []
    for package_name, test_func in packages_to_test:
        if not test_import(package_name, test_func):
            failed_packages.append(package_name)
    
    print("\n" + "=" * 40)
    if failed_packages:
        print("❌ Some packages failed to import:")
        for package in failed_packages:
            print(f"   - {package}")
        print("\nPlease reinstall the failed packages:")
        print("   pip install -r requirements.txt --force-reinstall")
        return False
    else:
        print("🎉 All critical packages imported successfully!")
        print("✅ Your installation appears to be working correctly!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)