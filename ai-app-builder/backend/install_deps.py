#!/usr/bin/env python3
"""
Script to help install or reinstall dependencies
"""
import os
import sys
import subprocess
import time

def check_python_path():
    """Check Python path and identify potential conflicts"""
    print("Checking Python environment...")
    print(f"Python executable: {sys.executable}")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"In virtual environment: {in_venv}")
    if in_venv:
        print(f"Virtual environment: {sys.prefix}")
    
    # Check for user site-packages conflicts
    user_site_conflict = False
    for path in sys.path:
        if 'Roaming' in path and 'Python' in path and 'site-packages' in path:
            print(f"⚠️  User site-packages detected: {path}")
            user_site_conflict = True
    
    if user_site_conflict:
        print("⚠️  Potential conflict with user site-packages detected!")
        print("   This may cause import issues with packages")
    
    return in_venv, user_site_conflict

def check_python():
    """Check if Python is available"""
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True, timeout=10)
        print(f"✅ Python version: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ Error checking Python: {e}")
        return False

def upgrade_pip():
    """Upgrade pip to the latest version"""
    try:
        print("Upgrading pip...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                              capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print("✅ Pip upgraded successfully!")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("⚠️  Error upgrading pip:")
            if result.stderr:
                print(result.stderr)
            # Continue anyway
            return True
    except Exception as e:
        print(f"⚠️  Error upgrading pip: {e}")
        # Continue anyway
        return True

def install_package(package_name, version=None, no_deps=False, no_cache=False):
    """Install a single package"""
    try:
        cmd = [sys.executable, "-m", "pip", "install"]
        if version:
            cmd.append(f"{package_name}=={version}")
        else:
            cmd.append(package_name)
            
        if no_deps:
            cmd.append("--no-deps")
        if no_cache:
            cmd.append("--no-cache-dir")
            
        print(f"Installing {package_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✅ {package_name} installed successfully!")
            return True
        else:
            print(f"❌ Error installing {package_name}:")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error installing {package_name}: {e}")
        return False

def install_pydantic_packages():
    """Install Pydantic packages with special handling"""
    print("\nInstalling Pydantic packages with special handling...")
    
    pydantic_packages = [
        ("pydantic", "2.5.0"),
        ("pydantic-settings", "2.1.0")
    ]
    
    for package, version in pydantic_packages:
        # Try multiple approaches
        approaches = [
            (f"{package}=={version}", False, False),
            (f"{package}=={version} --force-reinstall", False, False),
            (f"{package}=={version} --force-reinstall --no-cache-dir", False, False),
            (f"{package}=={version} --force-reinstall --no-deps", True, False),
        ]
        
        installed = False
        for approach_cmd, no_deps, no_cache in approaches:
            print(f"Trying to install {package}=={version}...")
            if install_package(package, version, no_deps, no_cache):
                installed = True
                break
        
        if not installed:
            print(f"❌ Failed to install {package}=={version}")
            return False
    
    return True

def install_from_requirements():
    """Install all packages from requirements.txt"""
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    
    if not os.path.exists(requirements_path):
        print(f"❌ requirements.txt not found at {requirements_path}")
        return False
    
    try:
        print("Installing packages from requirements.txt...")
        # Use --force-reinstall to ensure correct versions
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--force-reinstall"],
                              capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            print("✅ All packages installed successfully!")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Error installing packages:")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running pip install: {e}")
        return False

def install_packages_individually():
    """Install packages one by one if bulk install fails"""
    packages = [
        ("fastapi", "0.104.1"),
        ("uvicorn[standard]", "0.24.0"),
        ("sqlalchemy", "2.0.35"),
        ("pymysql", "1.1.0"),
        ("python-multipart", "0.0.6"),
        ("python-jose[cryptography]", "3.3.0"),
        ("passlib[bcrypt]", "1.7.4"),
        ("python-dotenv", "1.0.0"),
        # Handle Pydantic separately
        ("alembic", "1.13.0"),
        ("httpx", "0.25.2"),
        ("openai", "1.3.7"),
        ("google-generativeai", "0.3.2"),
        ("google-auth", "2.23.4"),
        ("google-auth-oauthlib", "1.1.0"),
        ("google-auth-httplib2", "0.1.1"),
        ("google-api-python-client", "2.108.0"),
        ("stripe", "7.8.0"),
        ("jinja2", "3.1.2"),
        ("aiofiles", "23.2.1"),
        ("docker", "6.1.3"),
        ("gitpython", "3.1.40"),
        ("requests", "2.31.0"),
        # Add typing_extensions for Python 3.13 compatibility
        ("typing_extensions", None)
    ]
    
    failed_packages = []
    
    # Install non-Pydantic packages first
    for package, version in packages:
        print(f"\n[{len(failed_packages) + 1}/{len(packages) + 2}] Installing {package}{f'=={version}' if version else ''}")
        if not install_package(package, version):
            failed_packages.append((package, version))
        # Small delay to avoid overwhelming the package index
        time.sleep(0.5)
    
    # Install Pydantic packages with special handling
    print(f"\n[{len(failed_packages) + 1}/{len(packages) + 2}] Installing Pydantic packages")
    if not install_pydantic_packages():
        failed_packages.append(("pydantic", "2.5.0"))
        failed_packages.append(("pydantic-settings", "2.1.0"))
    
    if failed_packages:
        print(f"\n⚠️  Failed to install {len(failed_packages)} packages:")
        for package, version in failed_packages:
            print(f"   - {package}{f'=={version}' if version else ''}")
        return False
    else:
        print("\n🎉 All packages installed successfully!")
        return True

def verify_installation():
    """Verify that packages can be imported"""
    packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("sqlalchemy", "sqlalchemy"),
        ("pymysql", "pymysql"),
        ("jose", "python-jose"),
        ("passlib", "passlib"),
        ("dotenv", "python-dotenv"),
        ("pydantic", "pydantic"),
        ("pydantic_settings", "pydantic-settings"),
        ("httpx", "httpx"),
        ("openai", "openai"),
        ("google.generativeai", "google-generativeai"),
        ("google.auth", "google-auth"),
        ("stripe", "stripe"),
        ("jinja2", "jinja2"),
    ]
    
    print("\nVerifying package installations...")
    print("=" * 50)
    failed_imports = []
    warnings = []
    
    for package_display, package_import in packages:
        try:
            module = __import__(package_import)
            # Special check for SQLAlchemy compatibility
            if package_display == "sqlalchemy":
                try:
                    from sqlalchemy import create_engine
                    print(f"✅ {package_display:<20}")
                except Exception as e:
                    if "SQLCoreOperations" in str(e) or "TypingOnly" in str(e):
                        print(f"⚠️  {package_display:<20} (Compatibility issue detected)")
                        warnings.append((package_display, package_import, "SQLAlchemy compatibility issue"))
                    else:
                        print(f"✅ {package_display:<20}")
            # Special check for Pydantic
            elif package_display == "pydantic":
                print(f"✅ {package_display:<20} (version {module.__version__})")
            # Special handling for packages with typing.Annotated issues
            elif package_display in ["fastapi", "openai"]:
                print(f"⚠️  {package_display:<20} (May have typing.Annotated issues)")
                warnings.append((package_display, package_import, "Potential typing.Annotated issue"))
            else:
                print(f"✅ {package_display:<20}")
        except ImportError as e:
            print(f"❌ {package_display:<20} (ImportError: {e})")
            failed_imports.append((package_display, package_import, str(e)))
        except Exception as e:
            # Handle the specific SQLAlchemy error
            if package_display == "sqlalchemy" and ("SQLCoreOperations" in str(e) or "TypingOnly" in str(e)):
                print(f"⚠️  {package_display:<20} (Compatibility issue detected)")
                warnings.append((package_display, package_import, "SQLAlchemy compatibility issue"))
            # Handle typing.Annotated issues
            elif "typing.Annotated" in str(e):
                print(f"⚠️  {package_display:<20} (typing.Annotated issue)")
                warnings.append((package_display, package_import, "typing.Annotated compatibility issue"))
            else:
                print(f"⚠️  {package_display:<20} (Error: {e})")
                failed_imports.append((package_display, package_import, str(e)))
    
    # Special check for pydantic internal modules
    print("\nChecking Pydantic compatibility...")
    try:
        import pydantic
        print(f"✅ Pydantic version: {pydantic.__version__}")
        
        # Check if this version has the _internal module
        try:
            from pydantic import _internal
            print("✅ pydantic._internal is available")
        except ImportError:
            # This is OK for some versions
            print("ℹ️  pydantic._internal not available (may be OK for this version)")
    except ImportError as e:
        print(f"❌ Pydantic import failed: {e}")
        failed_imports.append(("pydantic", "pydantic", str(e)))
    
    if failed_imports:
        print(f"\n❌ Failed to import {len(failed_imports)} packages")
        return False
    elif warnings:
        print(f"\n⚠️  {len(warnings)} packages have compatibility warnings")
        print("These may cause issues but might still work.")
        return True
    else:
        print("\n🎉 All packages imported successfully!")
        return True

def fix_sqlalchemy_issues():
    """Try to fix common SQLAlchemy compatibility issues"""
    print("\nAttempting to fix SQLAlchemy compatibility issues...")
    
    # Try different approaches to fix SQLAlchemy
    approaches = [
        ("Reinstalling SQLAlchemy", ["sqlalchemy==2.0.35", "--force-reinstall"]),
        ("Reinstalling with --no-cache-dir", ["sqlalchemy==2.0.35", "--force-reinstall", "--no-cache-dir"]),
        ("Installing with --no-deps", ["sqlalchemy==2.0.35", "--force-reinstall", "--no-deps"]),
        ("Installing older compatible version", ["sqlalchemy==1.4.46", "--force-reinstall"]),
    ]
    
    for approach_name, install_args in approaches:
        print(f"\n{approach_name}...")
        try:
            cmd = [sys.executable, "-m", "pip", "install"] + install_args
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print(f"✅ {approach_name} completed successfully!")
                return True
            else:
                print(f"❌ {approach_name} failed:")
                if result.stderr:
                    print(result.stderr)
        except Exception as e:
            print(f"❌ Error during {approach_name}: {e}")
    
    return False

def fix_environment_conflicts():
    """Fix environment conflicts specifically"""
    print("\nAttempting to fix environment conflicts...")
    
    # Try to disable user site-packages
    print("Setting PYTHONNOUSERSITE=1...")
    env = os.environ.copy()
    env['PYTHONNOUSERSITE'] = '1'
    
    try:
        # Reinstall SQLAlchemy with user site-packages disabled
        cmd = [sys.executable, "-m", "pip", "install", "sqlalchemy==2.0.23", "--force-reinstall"]
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ SQLAlchemy reinstalled with user site-packages disabled!")
            return True
        else:
            print("❌ Error reinstalling SQLAlchemy with user site-packages disabled:")
            if result.stderr:
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during environment conflict fix: {e}")
        return False

def fix_pydantic_issues():
    """Try to fix common Pydantic compatibility issues"""
    print("\nAttempting to fix Pydantic compatibility issues...")
    
    # Try to reinstall pydantic and pydantic-settings specifically
    return install_pydantic_packages()

if __name__ == "__main__":
    print("AI App Builder - Dependency Installation Helper")
    print("=" * 50)
    
    # Check environment
    in_venv, user_site_conflict = check_python_path()
    
    if not in_venv:
        print("⚠️  Not running in a virtual environment!")
        print("   This may cause conflicts with user site-packages")
    
    if user_site_conflict:
        print("⚠️  User site-packages conflict detected!")
        print("   This may cause import issues")
    
    # Check Python
    if not check_python():
        print("❌ Python not found. Please ensure Python is installed.")
        sys.exit(1)
    
    # Upgrade pip first
    print("\nStep 1: Upgrading pip...")
    if not upgrade_pip():
        print("⚠️  Continuing without pip upgrade...")
    
    # Try installing from requirements.txt first
    print("\nStep 2: Installing from requirements.txt...")
    if install_from_requirements():
        print("\n✅ Installation from requirements.txt completed!")
    else:
        print("\n⚠️  Installing from requirements.txt failed. Trying individual installation...")
        if not install_packages_individually():
            print("\n💥 Failed to install dependencies.")
            sys.exit(1)
    
    # Verify installation
    print("\nStep 3: Verifying installation...")
    verification_result = verify_installation()
    
    if not verification_result:
        print("\n⚠️  Some packages could not be imported.")
        
        # Try to fix specific issues
        try:
            import sqlalchemy
            print("\nAttempting to fix SQLAlchemy issues...")
            if fix_sqlalchemy_issues():
                print("Retrying verification...")
                if not verify_installation():
                    print("\n💥 Verification still failed after fixes.")
                    # Try environment conflict fix
                    if fix_environment_conflicts():
                        print("Retrying verification after environment fix...")
                        if not verify_installation():
                            print("\n💥 Verification still failed after environment fix.")
                            sys.exit(1)
                    else:
                        sys.exit(1)
                else:
                    print("\n✅ Verification successful after SQLAlchemy fixes!")
            else:
                print("\n💥 Failed to fix SQLAlchemy issues.")
                sys.exit(1)
        except ImportError:
            pass  # SQLAlchemy not installed, will be handled by general installation
            
        try:
            import pydantic
            print("\nAttempting to fix Pydantic issues...")
            if fix_pydantic_issues():
                print("Retrying verification...")
                if not verify_installation():
                    print("\n💥 Verification still failed after fixes.")
                    sys.exit(1)
                else:
                    print("\n✅ Verification successful after Pydantic fixes!")
            else:
                print("\n💥 Failed to fix Pydantic issues.")
                sys.exit(1)
        except ImportError:
            pass  # Pydantic not installed, will be handled by general installation
            
        sys.exit(1)
    
    print("\n🎉 All dependencies installed and verified successfully!")
    print("You can now run the network connectivity tests.")
        
    print("\n💡 Tip: If you still have issues, try:")
    print("   1. Closing and reopening your terminal")
    print("   2. Deactivating and reactivating your virtual environment")
    print("   3. Running this script again")
    if user_site_conflict:
        print("   4. Consider removing user site-packages packages that conflict:")
        print("      pip uninstall sqlalchemy pydantic --user")