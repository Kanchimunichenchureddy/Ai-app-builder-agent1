#!/usr/bin/env python3
"""
Script to update SQLAlchemy to a Python 3.13 compatible version
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
    print("🔧 Updating SQLAlchemy to Python 3.13 compatible version...")
    
    # Get the backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(backend_dir, "venv")
    requirements_file = os.path.join(backend_dir, "requirements.txt")
    
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
    
    # First, try to uninstall existing SQLAlchemy
    print("🗑️  Uninstalling existing SQLAlchemy...")
    success, stdout, stderr = run_command(f'"{pip_cmd}" uninstall sqlalchemy -y')
    if not success:
        print(f"Warning: Could not uninstall SQLAlchemy: {stderr}")
    
    # Install the updated SQLAlchemy
    print("📥 Installing SQLAlchemy 2.0.35...")
    success, stdout, stderr = run_command(f'"{pip_cmd}" install sqlalchemy==2.0.35')
    
    if success:
        print("✅ SQLAlchemy 2.0.35 installed successfully!")
        
        # Test the import
        print("🧪 Testing SQLAlchemy import...")
        try:
            import sqlalchemy
            print(f"✅ SQLAlchemy import successful! Version: {sqlalchemy.__version__}")
            return True
        except Exception as e:
            print(f"❌ SQLAlchemy import failed: {e}")
            return False
    else:
        print(f"❌ Failed to install SQLAlchemy: {stderr}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)