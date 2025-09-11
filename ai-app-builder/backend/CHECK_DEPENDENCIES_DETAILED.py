#!/usr/bin/env python3
"""
Script to check if all required dependencies are installed with detailed information
"""

import sys
import importlib
import subprocess

def get_package_version(package_name):
    """Get the version of an installed package"""
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "show", package_name
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    return line.split(':', 1)[1].strip()
        return "Unknown"
    except:
        return "Unknown"

def check_package(package_name, version=None, install_name=None):
    """Check if a package is installed"""
    if install_name is None:
        install_name = package_name
    
    try:
        package = importlib.import_module(package_name)
        installed_version = getattr(package, '__version__', 'Unknown')
        if installed_version == 'Unknown':
            installed_version = get_package_version(install_name)
        
        if version:
            print(f"✅ {package_name} ({installed_version}) - Required: {version}")
        else:
            print(f"✅ {package_name} ({installed_version})")
        return True
    except ImportError:
        print(f"❌ {package_name} (NOT INSTALLED)")
        return False
    except Exception as e:
        print(f"❌ {package_name} (ERROR: {str(e)})")
        return False

def main():
    print("AI App Builder - Detailed Dependency Check")
    print("=" * 45)
    
    required_packages = [
        ('fastapi', '0.104.1'),
        ('uvicorn', '0.24.0'),
        ('sqlalchemy', '2.0.35'),
        ('pymysql', '1.1.0'),
        ('multipart', '0.0.6', 'python-multipart'),
        ('jose', '3.3.0', 'python-jose'),
        ('passlib', '1.7.4'),
        ('dotenv', '1.0.0', 'python-dotenv'),
        ('pydantic', '2.5.0'),
        ('pydantic_settings', '2.1.0', 'pydantic-settings'),
        ('httpx', '0.25.2'),
        ('requests', '2.31.0'),
        ('stripe', '7.8.0'),
        ('jinja2', '3.1.2'),
        ('aiofiles', '23.2.1'),
        ('docker', '6.1.3'),
        ('git', '3.1.40', 'gitpython')
    ]
    
    print("\nChecking required packages:")
    print("-" * 30)
    
    missing_packages = []
    for package_info in required_packages:
        if len(package_info) == 2:
            package_name, version = package_info
            install_name = None
        else:
            package_name, version, install_name = package_info
            
        if not check_package(package_name, version, install_name):
            if install_name:
                missing_packages.append((package_name, install_name))
            else:
                missing_packages.append((package_name, package_name))
    
    print("\n" + "=" * 45)
    if missing_packages:
        print("⚠️  Some packages are missing:")
        for package_name, install_name in missing_packages:
            print(f"   - {package_name} (install with: pip install {install_name})")
        print("\nQuick installation options:")
        print("   Option 1 - Install individual missing packages:")
        missing_install_names = [install_name for _, install_name in missing_packages]
        print(f"      pip install {' '.join(missing_install_names)}")
        print("\n   Option 2 - Install all dependencies:")
        print("      pip install -r requirements.txt")
        print("\n   Option 3 - Use the auto-install scripts:")
        print("      Double-click AUTO_INSTALL_DEPS.bat")
        print("      Or run: .\\AUTO_INSTALL_DEPS.ps1 (in PowerShell)")
    else:
        print("🎉 All required packages are installed!")
        print("✅ Your environment is ready to run the AI App Builder backend!")

if __name__ == "__main__":
    main()