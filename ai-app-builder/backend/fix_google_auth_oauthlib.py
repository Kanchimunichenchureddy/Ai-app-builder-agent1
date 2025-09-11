#!/usr/bin/env python3
"""
Script to fix google-auth-oauthlib package import issues
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
    print("🔧 Fixing google-auth-oauthlib package import issues...")
    
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
    
    package = "google-auth-oauthlib"
    version = "1.2.0"  # Use the newer version
    
    print(f"\n🔧 Fixing {package}...")
    
    # First, uninstall the package
    print(f"🗑️  Uninstalling {package}...")
    success, stdout, stderr = run_command(f'"{pip_cmd}" uninstall "{package}" -y')
    if not success:
        print(f"Warning: Could not uninstall {package}: {stderr}")
    
    # Try multiple installation approaches
    install_approaches = [
        f'"{pip_cmd}" install "{package}=={version}" --force-reinstall --no-cache-dir',
        f'"{pip_cmd}" install "{package}=={version}" --force-reinstall',
        f'"{pip_cmd}" install "{package}" --force-reinstall --no-cache-dir',
        f'"{pip_cmd}" install "{package}" --force-reinstall',
        # Try installing without version specification
        f'"{pip_cmd}" install "{package}"',
    ]
    
    installed = False
    for i, install_cmd in enumerate(install_approaches):
        print(f"Attempt {i+1}: {install_cmd}")
        success, stdout, stderr = run_command(install_cmd)
        
        if success:
            print(f"✅ {package} installed successfully!")
            installed = True
            break
        else:
            print(f"❌ Attempt {i+1} failed: {stderr}")
    
    if not installed:
        print(f"❌ Failed to install {package}")
        return False
        
    # Test the import
    print(f"🧪 Testing {package} import...")
    try:
        import google.auth.oauthlib
        print(f"✅ {package} import successful!")
        print(f"✅ google.auth.oauthlib module loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ {package} import failed: {e}")
        # Try alternative import
        try:
            import google_auth_oauthlib
            print(f"✅ Alternative import successful!")
            return True
        except Exception as e2:
            print(f"❌ Alternative import also failed: {e2}")
            return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 google-auth-oauthlib fixed successfully!")
    else:
        print("\n💥 Failed to fix google-auth-oauthlib.")
        print("\n💡 Manual fix options:")
        print("1. Try installing with specific index:")
        print("   pip install google-auth-oauthlib==1.2.0 --force-reinstall --no-cache-dir -i https://pypi.org/simple/")
        print("2. Try installing without version:")
        print("   pip install google-auth-oauthlib --force-reinstall --no-cache-dir")
        print("3. Check if there are conflicting packages:")
        print("   pip list | findstr google")
    sys.exit(0 if success else 1)