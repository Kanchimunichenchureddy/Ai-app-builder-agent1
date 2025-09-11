#!/usr/bin/env python3
"""
Emergency script to downgrade SQLAlchemy to a version compatible with Python 3.13
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
    print("🔧 Emergency SQLAlchemy downgrade for Python 3.13 compatibility...")
    
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
    
    # Try to uninstall current SQLAlchemy
    print("\n🗑️  Uninstalling current SQLAlchemy...")
    success, stdout, stderr = run_command(f'"{pip_cmd}" uninstall sqlalchemy -y')
    if not success:
        print(f"Warning: Could not uninstall SQLAlchemy: {stderr}")
    
    # Try multiple versions of SQLAlchemy that might work with Python 3.13
    sqlalchemy_versions = [
        "2.0.35",  # Our updated version
        "2.0.30",  # Slightly older version
        "2.0.25",  # Even older version
        "1.4.46",  # Last 1.4.x version
        "1.4.41",  # Known stable version
    ]
    
    for version in sqlalchemy_versions:
        print(f"\n📥 Trying SQLAlchemy {version}...")
        install_cmd = f'"{pip_cmd}" install "sqlalchemy=={version}" --force-reinstall --no-cache-dir'
        success, stdout, stderr = run_command(install_cmd)
        
        if success:
            print(f"✅ SQLAlchemy {version} installed successfully!")
            
            # Test the import
            print(f"🧪 Testing SQLAlchemy {version} import...")
            try:
                # Test import in a separate process to avoid conflicts
                test_code = f"""
import sys
import os
os.environ['PYTHONNOUSERSITE'] = '1'
try:
    import sqlalchemy
    print(f"SUCCESS: SQLAlchemy version {{sqlalchemy.__version__}}")
    sys.exit(0)
except Exception as e:
    print(f"ERROR: {{e}}")
    sys.exit(1)
"""
                
                result = subprocess.run(
                    [sys.executable, "-c", test_code],
                    capture_output=True, 
                    text=True, 
                    timeout=60,
                    env={**os.environ, 'PYTHONNOUSERSITE': '1'}
                )
                
                if result.returncode == 0:
                    print(f"✅ SQLAlchemy {version} import test succeeded!")
                    print(result.stdout)
                    return True
                else:
                    print(f"❌ SQLAlchemy {version} import test failed:")
                    print(result.stdout)
                    print(result.stderr)
            except Exception as e:
                print(f"❌ Error during verification: {e}")
        else:
            print(f"❌ Failed to install SQLAlchemy {version}: {stderr}")
    
    print("\n💥 All SQLAlchemy versions failed to install properly.")
    return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 SQLAlchemy downgrade completed successfully!")
        print("\nNext steps:")
        print("1. Test SQLAlchemy import:")
        print("   python -c \"import sqlalchemy; print(sqlalchemy.__version__)\"")
        print("2. Run the backend:")
        print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("\n💥 Emergency SQLAlchemy downgrade failed.")
        print("\n💡 Manual fix options:")
        print("1. Try installing a specific older version:")
        print("   pip install sqlalchemy==1.4.41 --force-reinstall --no-cache-dir")
        print("2. Check if there are conflicting packages:")
        print("   pip list | findstr sqlalchemy")
    sys.exit(0 if success else 1)