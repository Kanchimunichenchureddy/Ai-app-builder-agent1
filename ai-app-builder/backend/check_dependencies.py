#!/usr/bin/env python3
"""
Script to check if all required dependencies are installed
"""

import sys
import importlib

def check_package(package_name, import_name=None, version=None):
    """Check if a package is installed"""
    # Use the import_name if provided, otherwise use package_name
    name_to_import = import_name if import_name else package_name
    
    try:
        package = importlib.import_module(name_to_import)
        if version and hasattr(package, '__version__'):
            print(f"✅ {package_name} ({package.__version__})")
        else:
            print(f"✅ {package_name}")
        return True
    except ImportError:
        print(f"❌ {package_name} (NOT INSTALLED)")
        return False

def main():
    print("AI App Builder - Dependency Check")
    print("=" * 35)
    
    # List of required packages with their import names
    required_packages = [
        ('fastapi', None, None),
        ('uvicorn', None, None),
        ('sqlalchemy', None, None),
        ('pymysql', None, None),
        ('python-multipart', 'multipart', None),  # Different import name
        ('python-jose', 'jose', None),            # Different import name
        ('passlib', None, None),
        ('python-dotenv', 'dotenv', None),        # Different import name
        ('pydantic', None, None),
        ('pydantic-settings', 'pydantic_settings', None),  # Different import name
        ('httpx', None, None),
        ('requests', None, None),
        ('stripe', None, None),
        ('jinja2', None, None),
        ('aiofiles', None, None),
        ('docker', None, None),
        ('gitpython', 'git', None)                # Different import name
    ]
    
    print("\nChecking required packages:")
    print("-" * 30)
    
    missing_packages = []
    for package_name, import_name, version in required_packages:
        if not check_package(package_name, import_name, version):
            missing_packages.append(package_name)
    
    print("\n" + "=" * 35)
    if missing_packages:
        print("⚠️  Some packages are missing:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall missing packages with:")
        print("   pip install -r requirements.txt")
        print("   OR install individually:")
        print("   pip install python-multipart python-jose[cryptography] python-dotenv pydantic-settings gitpython")
        return False
    else:
        print("🎉 All required packages are installed!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)