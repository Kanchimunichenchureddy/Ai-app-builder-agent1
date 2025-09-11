#!/usr/bin/env python3
"""
Script to fix Pydantic installation issues
"""
import sys
import subprocess
import os

def check_pydantic():
    """Check Pydantic installation"""
    try:
        import pydantic
        print(f"✅ Pydantic is installed, version: {pydantic.__version__}")
        
        # Check if _internal module is available
        try:
            from pydantic import _internal
            print("✅ pydantic._internal is available")
        except ImportError:
            print("ℹ️  pydantic._internal is not available (may be OK for this version)")
        
        return True
    except ImportError as e:
        print(f"❌ Pydantic is not installed: {e}")
        return False
    except Exception as e:
        print(f"❌ Pydantic import error: {e}")
        return False

def install_pydantic_version(version="2.5.0"):
    """Install specific Pydantic version"""
    print(f"Installing Pydantic version {version}...")
    
    # Try multiple approaches
    approaches = [
        f"pydantic=={version}",
        f"pydantic=={version} --force-reinstall",
        f"pydantic=={version} --force-reinstall --no-cache-dir",
        f"pydantic=={version} --force-reinstall --no-deps",
    ]
    
    for i, approach in enumerate(approaches, 1):
        print(f"\nAttempt {i}: pip install {approach}")
        try:
            cmd = [sys.executable, "-m", "pip", "install"] + approach.split()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ Pydantic {version} installed successfully!")
                if result.stdout:
                    print(result.stdout)
                return True
            else:
                print(f"❌ Attempt {i} failed:")
                if result.stderr:
                    print(result.stderr)
        except Exception as e:
            print(f"❌ Error during attempt {i}: {e}")
    
    return False

def fix_pydantic_environment():
    """Fix Pydantic environment issues"""
    print("Attempting to fix Pydantic environment issues...")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"In virtual environment: {in_venv}")
    
    # Check for user site-packages conflicts
    user_site_conflict = False
    for path in sys.path:
        if 'Roaming' in path and 'Python' in path and 'site-packages' in path:
            print(f"⚠️  User site-packages detected: {path}")
            user_site_conflict = True
    
    if user_site_conflict:
        print("⚠️  User site-packages conflict detected!")
        print("   Setting PYTHONNOUSERSITE=1 to disable user site-packages")
        env = os.environ.copy()
        env['PYTHONNOUSERSITE'] = '1'
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "pydantic==2.5.0", "--force-reinstall"
            ], env=env, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ Pydantic installed with user site-packages disabled!")
                return True
            else:
                print("❌ Failed to install Pydantic with user site-packages disabled:")
                if result.stderr:
                    print(result.stderr)
        except Exception as e:
            print(f"❌ Error during installation with user site-packages disabled: {e}")
    
    return False

def clean_pydantic_install():
    """Clean install Pydantic"""
    print("Attempting clean Pydantic installation...")
    
    # First uninstall
    print("Uninstalling Pydantic...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "uninstall", 
            "pydantic", "pydantic-settings", "-y"
        ], capture_output=True, text=True, timeout=120)
    except Exception as e:
        print(f"Warning during uninstall: {e}")
    
    # Then reinstall
    return install_pydantic_version("2.5.0")

def check_compatibility():
    """Check compatibility with other packages"""
    print("Checking compatibility with related packages...")
    
    related_packages = [
        ("pydantic-settings", "2.1.0"),
        ("pydantic_core", None),
        ("typing_extensions", None),
    ]
    
    for package, version in related_packages:
        try:
            __import__(package.replace("-", "_"))
            if version:
                module = __import__(package.replace("-", "_"))
                installed_version = getattr(module, '__version__', 'Unknown')
                print(f"✅ {package} version {installed_version} is installed")
            else:
                print(f"✅ {package} is installed")
        except ImportError:
            if version:
                print(f"⚠️  {package}=={version} is not installed")
            else:
                print(f"⚠️  {package} is not installed")

if __name__ == "__main__":
    print("Pydantic Installation Fixer")
    print("=" * 30)
    
    # Check current status
    if check_pydantic():
        print("\n🎉 Pydantic is already working!")
        check_compatibility()
    else:
        print("\nAttempting to fix Pydantic installation...")
        
        # Try different approaches
        approaches = [
            ("Install specific version", lambda: install_pydantic_version("2.5.0")),
            ("Fix environment conflicts", fix_pydantic_environment),
            ("Clean installation", clean_pydantic_install),
        ]
        
        for approach_name, approach_func in approaches:
            print(f"\nTrying approach: {approach_name}")
            if approach_func():
                print(f"✅ {approach_name} succeeded!")
                # Verify installation
                if check_pydantic():
                    print("\n🎉 Pydantic is now working!")
                    check_compatibility()
                    break
            else:
                print(f"❌ {approach_name} failed")
        else:
            print("\n💥 All approaches failed. Manual intervention required.")
            print("\n💡 Manual fix options:")
            print("   1. Try installing with specific index:")
            print("      pip install pydantic==2.5.0 -i https://pypi.org/simple/")
            print("   2. Try installing without dependencies:")
            print("      pip install pydantic==2.5.0 --no-deps")
            print("   3. Check for conflicting packages:")
            print("      pip list | findstr pydantic")