#!/usr/bin/env python3
"""
Emergency script to fix SQLAlchemy import issues
This script avoids importing SQLAlchemy directly and works at the pip level
"""
import sys
import subprocess
import os

def check_virtual_environment():
    """Check if we're in the correct virtual environment"""
    print("Checking virtual environment...")
    
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"In virtual environment: {in_venv}")
    
    if in_venv:
        print(f"Virtual environment path: {sys.prefix}")
    
    return in_venv

def disable_user_site_packages():
    """Set environment variable to disable user site-packages"""
    print("Setting PYTHONNOUSERSITE=1 to disable user site-packages...")
    os.environ['PYTHONNOUSERSITE'] = '1'
    print("User site-packages disabled for this session")

def run_pip_command(command_args):
    """Run a pip command safely"""
    try:
        cmd = [sys.executable, "-m", "pip"] + command_args
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Command succeeded")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Command failed:")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def emergency_sqlalchemy_fix():
    """Emergency fix for SQLAlchemy import issues"""
    print("Emergency SQLAlchemy Fix")
    print("=" * 30)
    
    # Check virtual environment
    in_venv = check_virtual_environment()
    
    # Disable user site-packages
    disable_user_site_packages()
    
    # Try to uninstall any existing SQLAlchemy
    print("\n1. Uninstalling existing SQLAlchemy...")
    run_pip_command(["uninstall", "sqlalchemy", "-y"])
    
    # Try multiple installation approaches
    print("\n2. Installing SQLAlchemy with different approaches...")
    
    approaches = [
        ["install", "sqlalchemy==2.0.35", "--force-reinstall"],
        ["install", "sqlalchemy==2.0.35", "--force-reinstall", "--no-cache-dir"],
        ["install", "sqlalchemy==1.4.46", "--force-reinstall"],  # Try older version
        ["install", "sqlalchemy==2.0.35", "--force-reinstall", "--no-deps"],
    ]
    
    for i, approach in enumerate(approaches, 1):
        print(f"\nAttempt {i}: {' '.join(approach)}")
        if run_pip_command(approach):
            print(f"✅ Attempt {i} succeeded!")
            return True
        else:
            print(f"❌ Attempt {i} failed")
    
    return False

def clean_install_all():
    """Clean install of all problematic packages"""
    print("\n3. Clean installing all potentially problematic packages...")
    
    packages = [
        "sqlalchemy==2.0.35",
        "pydantic==2.5.0", 
        "pydantic-settings==2.1.0"
    ]
    
    for package in packages:
        print(f"\nUninstalling {package}...")
        run_pip_command(["uninstall", package.split('==')[0], "-y"])
        
        print(f"Installing {package}...")
        if not run_pip_command(["install", package, "--force-reinstall", "--no-cache-dir"]):
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def verify_fix():
    """Verify the fix by trying to import SQLAlchemy in a subprocess"""
    print("\n4. Verifying fix...")
    
    try:
        # Test import in a separate process to avoid conflicts
        test_code = """
import sys
import os
os.environ['PYTHONNOUSERSITE'] = '1'
try:
    import sqlalchemy
    print(f"SUCCESS: SQLAlchemy version {sqlalchemy.__version__}")
    sys.exit(0)
except Exception as e:
    print(f"ERROR: {e}")
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
            print("✅ SQLAlchemy import test succeeded!")
            print(result.stdout)
            return True
        else:
            print("❌ SQLAlchemy import test failed:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

if __name__ == "__main__":
    print("Emergency SQLAlchemy Import Fix")
    print("=" * 40)
    
    # Try the emergency fix
    if emergency_sqlalchemy_fix():
        print("\n✅ Emergency fix completed!")
        
        # Try clean installation of related packages
        if clean_install_all():
            print("\n✅ Clean installation completed!")
            
            # Verify the fix
            if verify_fix():
                print("\n🎉 All fixes successful! SQLAlchemy should now work correctly.")
                print("\nNext steps:")
                print("1. Test SQLAlchemy import:")
                print("   python -c \"import sqlalchemy; print(sqlalchemy.__version__)\"")
                print("2. Run dependency installation:")
                print("   python install_deps.py")
            else:
                print("\n⚠️  Emergency fix completed but verification failed.")
                print("Try running this script again or manually fix the environment.")
        else:
            print("\n❌ Clean installation failed.")
    else:
        print("\n❌ Emergency fix failed.")
        print("\n💡 Manual fix options:")
        print("1. Manually set environment variable and reinstall:")
        print("   set PYTHONNOUSERSITE=1")
        print("   pip uninstall sqlalchemy -y")
        print("   pip install sqlalchemy==2.0.35 --force-reinstall")
        print("2. Try installing an older compatible version:")
        print("   pip install sqlalchemy==1.4.46 --force-reinstall")