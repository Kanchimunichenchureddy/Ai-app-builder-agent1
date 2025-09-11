#!/usr/bin/env python3
"""
Script to fix SQLAlchemy environment conflicts
"""
import sys
import os
import subprocess

def check_python_path():
    """Check Python path and identify SQLAlchemy locations"""
    print("Checking Python path...")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    # Check where SQLAlchemy is being imported from
    try:
        import sqlalchemy
        print(f"SQLAlchemy location: {sqlalchemy.__file__}")
        print(f"SQLAlchemy version: {sqlalchemy.__version__}")
    except Exception as e:
        print(f"Error importing SQLAlchemy: {e}")
    
    print("\nPython path:")
    for i, path in enumerate(sys.path):
        print(f"  {i}: {path}")
        
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"\nIn virtual environment: {in_venv}")
    if in_venv:
        print(f"Virtual environment: {sys.prefix}")

def check_site_packages():
    """Check site-packages directories"""
    print("\nChecking site-packages directories...")
    
    # Check for user site-packages
    if hasattr(sys, 'path') and sys.path:
        user_site = None
        for path in sys.path:
            if 'Roaming' in path and 'Python' in path and 'site-packages' in path:
                user_site = path
                break
        
        if user_site:
            print(f"⚠️  User site-packages detected: {user_site}")
            print("   This may conflict with your virtual environment")
            
            # Check if SQLAlchemy is in user site-packages
            sqlalchemy_user_path = os.path.join(user_site, 'sqlalchemy')
            if os.path.exists(sqlalchemy_user_path):
                print(f"⚠️  SQLAlchemy found in user site-packages: {sqlalchemy_user_path}")
                return user_site
    
    return None

def fix_environment():
    """Fix environment conflicts"""
    print("\nAttempting to fix environment conflicts...")
    
    # Check if we're in the correct virtual environment
    venv_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    venv_python = os.path.join(venv_path, 'venv', 'Scripts', 'python.exe')
    
    if os.path.exists(venv_python):
        print(f"✅ Virtual environment found: {venv_path}")
        print(f"✅ Virtual environment Python: {venv_python}")
    else:
        print(f"⚠️  Virtual environment not found at expected location: {venv_path}")
        return False
    
    # Try to reinstall SQLAlchemy in the virtual environment
    try:
        print("\nReinstalling SQLAlchemy in virtual environment...")
        result = subprocess.run([
            venv_python, "-m", "pip", "install", 
            "sqlalchemy==2.0.23", "--force-reinstall", "--no-deps"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ SQLAlchemy reinstalled in virtual environment!")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Error reinstalling SQLAlchemy:")
            if result.stderr:
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during SQLAlchemy reinstallation: {e}")
        return False

def disable_user_site_packages():
    """Try to disable user site-packages"""
    print("\nAttempting to disable user site-packages...")
    
    try:
        # Try to reinstall with user site-packages disabled
        env = os.environ.copy()
        env['PYTHONNOUSERSITE'] = '1'
        
        venv_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        venv_python = os.path.join(venv_path, 'venv', 'Scripts', 'python.exe')
        
        if os.path.exists(venv_python):
            result = subprocess.run([
                venv_python, "-m", "pip", "install", 
                "sqlalchemy==2.0.23", "--force-reinstall"
            ], env=env, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ SQLAlchemy reinstalled with user site-packages disabled!")
                return True
            else:
                print("❌ Error reinstalling SQLAlchemy with user site-packages disabled:")
                if result.stderr:
                    print(result.stderr)
                return False
        else:
            print("❌ Virtual environment Python not found")
            return False
            
    except Exception as e:
        print(f"❌ Error during reinstallation with user site-packages disabled: {e}")
        return False

def clean_install():
    """Clean install of all dependencies"""
    print("\nAttempting clean installation of all dependencies...")
    
    try:
        venv_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        venv_python = os.path.join(venv_path, 'venv', 'Scripts', 'python.exe')
        
        if os.path.exists(venv_python):
            # First, uninstall SQLAlchemy
            print("Uninstalling SQLAlchemy...")
            subprocess.run([
                venv_python, "-m", "pip", "uninstall", "sqlalchemy", "-y"
            ], capture_output=True, text=True, timeout=120)
            
            # Then reinstall with force
            print("Reinstalling SQLAlchemy...")
            result = subprocess.run([
                venv_python, "-m", "pip", "install", 
                "sqlalchemy==2.0.23", "--force-reinstall", "--no-cache-dir"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ SQLAlchemy clean installed!")
                return True
            else:
                print("❌ Error during clean installation:")
                if result.stderr:
                    print(result.stderr)
                return False
        else:
            print("❌ Virtual environment Python not found")
            return False
            
    except Exception as e:
        print(f"❌ Error during clean installation: {e}")
        return False

if __name__ == "__main__":
    print("SQLAlchemy Environment Conflict Fixer")
    print("=" * 40)
    
    # Check current environment
    check_python_path()
    user_site = check_site_packages()
    
    if user_site:
        print(f"\n⚠️  Conflict detected: SQLAlchemy is being imported from user site-packages")
        print(f"   Location: {user_site}")
        print("   This can cause compatibility issues with your virtual environment")
    
    print("\n" + "=" * 40)
    print("Attempting to fix environment conflicts...")
    
    # Try different approaches
    approaches = [
        ("Fix environment", fix_environment),
        ("Disable user site-packages", disable_user_site_packages),
        ("Clean installation", clean_install)
    ]
    
    for approach_name, approach_func in approaches:
        print(f"\nTrying approach: {approach_name}")
        if approach_func():
            print(f"✅ {approach_name} succeeded!")
            print("\nPlease test SQLAlchemy import:")
            print("   python -c \"import sqlalchemy; print(sqlalchemy.__version__)\"")
            break
        else:
            print(f"❌ {approach_name} failed")
    else:
        print("\n💥 All approaches failed. Manual intervention required.")
        print("\n💡 Manual fix options:")
        print("   1. Remove user site-packages SQLAlchemy:")
        print("      pip uninstall sqlalchemy --user")
        print("   2. Reinstall in virtual environment:")
        print("      venv\\Scripts\\pip install sqlalchemy==2.0.23 --force-reinstall")
        print("   3. Set PYTHONNOUSERSITE=1 environment variable")