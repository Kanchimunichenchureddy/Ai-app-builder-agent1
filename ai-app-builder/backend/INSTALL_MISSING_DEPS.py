#!/usr/bin/env python3
"""
Script to install missing dependencies
"""

import subprocess
import sys
import importlib

def check_and_install_package(package_name, install_name=None):
    """Check if a package is installed, and install it if not"""
    if install_name is None:
        install_name = package_name
    
    try:
        importlib.import_module(package_name)
        print(f"✅ {package_name} is already installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is missing, installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])
            print(f"✅ {package_name} installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package_name}: {e}")
            return False

def install_from_requirements():
    """Install all dependencies from requirements.txt"""
    print("Installing all dependencies from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install from requirements.txt: {e}")
        return False

def main():
    print("AI App Builder - Missing Dependency Installer")
    print("=" * 45)
    
    # List of missing packages from your check
    missing_packages = [
        ("multipart", "python-multipart"),
        ("jose", "python-jose[cryptography]"),
        ("dotenv", "python-dotenv"),
        ("pydantic_settings", "pydantic-settings"),
        ("git", "gitpython")
    ]
    
    print("\nOption 1: Install individual missing packages")
    print("-" * 45)
    
    all_installed = True
    for package_name, install_name in missing_packages:
        if not check_and_install_package(package_name, install_name):
            all_installed = False
    
    if all_installed:
        print("\n🎉 All missing packages installed successfully!")
        return
    
    print("\n" + "=" * 45)
    print("Option 2: Install all dependencies from requirements.txt")
    print("-" * 45)
    
    choice = input("Would you like to install all dependencies from requirements.txt? (y/n): ")
    if choice.lower() == 'y':
        if install_from_requirements():
            print("\n🎉 All dependencies installed successfully!")
        else:
            print("\n❌ Failed to install all dependencies")
            print("Please try manually running: pip install -r requirements.txt")
    else:
        print("\nPlease install the missing packages manually:")
        print("pip install python-multipart python-jose[cryptography] python-dotenv pydantic-settings gitpython")

if __name__ == "__main__":
    main()