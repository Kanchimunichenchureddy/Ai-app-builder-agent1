#!/usr/bin/env python3
"""
Script to fix package import issues with Python 3.13 compatibility
"""
import os
import subprocess
import sys

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True,
            timeout=300  # 5 minute timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def main():
    print("🔧 Fixing package import issues for Python 3.13 compatibility...")
    
    # Get the backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(backend_dir, "venv")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    # Determine pip command
    if in_venv:
        pip_cmd = "pip"
    elif os.path.exists(venv_dir):
        if os.name == 'nt':  # Windows
            pip_cmd = os.path.join(venv_dir, "Scripts", "pip.exe")
        else:  # Unix-like
            pip_cmd = os.path.join(venv_dir, "bin", "pip")
    else:
        pip_cmd = "pip"
    
    print(f"Using pip command: {pip_cmd}")
    
    # Set environment variable to disable user site-packages
    os.environ['PYTHONNOUSERSITE'] = '1'
    print("Disabled user site-packages")
    
    # Packages that need to be fixed
    packages_to_fix = [
        # FastAPI and related packages with typing.Annotated issues
        ("fastapi", "0.104.1"),
        ("openai", "1.3.7"),
        ("typing_extensions", None),  # For typing compatibility
        
        # Missing packages
        ("python-jose[cryptography]", "3.3.0"),
        ("python-dotenv", "1.0.0"),
        ("pydantic-settings", "2.1.0"),
        ("google-generativeai", "0.3.2"),
        ("google-auth", "2.23.4"),
        # Updated to more compatible versions for Python 3.13
        ("google-auth-oauthlib", "1.2.0"),
        ("google-auth-httplib2", "0.2.0"),
        ("google-api-python-client", "2.110.0"),
    ]
    
    failed_packages = []
    
    for package, version in packages_to_fix:
        package_name = package.split('[')[0]  # Get base package name
        print(f"\n🔧 Fixing {package}...")
        
        # First, uninstall the package
        print(f"🗑️  Uninstalling {package_name}...")
        success, stdout, stderr = run_command(f'"{pip_cmd}" uninstall "{package_name}" -y')
        if not success:
            print(f"Warning: Could not uninstall {package_name}: {stderr}")
        
        # Install the package
        if version:
            install_cmd = f'"{pip_cmd}" install "{package}=={version}" --force-reinstall --no-cache-dir'
        else:
            install_cmd = f'"{pip_cmd}" install "{package}" --force-reinstall --no-cache-dir'
            
        print(f"📥 Installing {package}...")
        success, stdout, stderr = run_command(install_cmd)
        
        if success:
            print(f"✅ {package} installed successfully!")
            
            # Test the import
            print(f"🧪 Testing {package_name} import...")
            try:
                if package_name == "python-jose":
                    import jose
                    print(f"✅ {package_name} import successful!")
                elif package_name == "python-dotenv":
                    import dotenv
                    print(f"✅ {package_name} import successful!")
                elif package_name == "pydantic-settings":
                    import pydantic_settings
                    print(f"✅ {package_name} import successful!")
                elif package_name == "google-generativeai":
                    import google.generativeai
                    print(f"✅ {package_name} import successful!")
                elif package_name == "google-auth":
                    import google.auth
                    print(f"✅ {package_name} import successful!")
                else:
                    # For other packages, just try importing by name
                    __import__(package_name)
                    print(f"✅ {package_name} import successful!")
            except Exception as e:
                print(f"❌ {package_name} import failed: {e}")
                failed_packages.append((package, version, str(e)))
        else:
            print(f"❌ Failed to install {package}: {stderr}")
            failed_packages.append((package, version, stderr))
    
    # Summary
    if failed_packages:
        print(f"\n❌ Failed to fix {len(failed_packages)} packages:")
        for package, version, error in failed_packages:
            print(f"   - {package}=={version}: {error}")
        return False
    else:
        print("\n🎉 All packages fixed successfully!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)