#!/usr/bin/env python3
"""
Script to fix Google authentication package import issues
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
    print("🔧 Fixing Google authentication package import issues...")
    
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
    
    # Google packages that need to be fixed
    google_packages = [
        ("google-auth-oauthlib", "1.1.0"),
        ("google-auth-httplib2", "0.1.1"),
        ("google-api-python-client", "2.108.0"),
    ]
    
    failed_packages = []
    
    for package, version in google_packages:
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
            failed_packages.append((package, version))
            continue
            
        # Test the import
        print(f"🧪 Testing {package} import...")
        try:
            if package == "google-auth-oauthlib":
                import google.auth.oauthlib
                print(f"✅ {package} import successful!")
            elif package == "google-auth-httplib2":
                import google_auth_httplib2
                print(f"✅ {package} import successful!")
            elif package == "google-api-python-client":
                import googleapiclient
                print(f"✅ {package} import successful!")
        except Exception as e:
            print(f"❌ {package} import failed: {e}")
            failed_packages.append((package, version))
    
    # Summary
    if failed_packages:
        print(f"\n❌ Failed to fix {len(failed_packages)} packages:")
        for package, version in failed_packages:
            print(f"   - {package}=={version}")
        return False
    else:
        print("\n🎉 All Google packages fixed successfully!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)