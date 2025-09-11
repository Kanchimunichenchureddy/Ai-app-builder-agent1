#!/usr/bin/env python3
"""
Script to check SQLAlchemy version and fix compatibility issues
"""
import sys

def check_sqlalchemy():
    """Check SQLAlchemy installation and version"""
    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy version: {sqlalchemy.__version__}")
        
        # Try to import key components
        try:
            from sqlalchemy import create_engine
            print("✅ SQLAlchemy create_engine is available")
        except Exception as e:
            print(f"❌ SQLAlchemy create_engine error: {e}")
            
        try:
            from sqlalchemy.orm import sessionmaker
            print("✅ SQLAlchemy sessionmaker is available")
        except Exception as e:
            print(f"❌ SQLAlchemy sessionmaker error: {e}")
            
        try:
            from sqlalchemy.ext.declarative import declarative_base
            print("✅ SQLAlchemy declarative_base is available")
        except Exception as e:
            print(f"❌ SQLAlchemy declarative_base error: {e}")
            
        return True
        
    except ImportError as e:
        print(f"❌ SQLAlchemy is not installed: {e}")
        return False
    except Exception as e:
        print(f"❌ SQLAlchemy error: {e}")
        return False

def fix_sqlalchemy():
    """Try to fix SQLAlchemy issues"""
    print("Attempting to fix SQLAlchemy issues...")
    
    try:
        # Try to reinstall SQLAlchemy with the correct version
        import subprocess
        import sys
        
        print("Reinstalling SQLAlchemy...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "sqlalchemy==2.0.23", "--force-reinstall"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ SQLAlchemy reinstalled successfully!")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Error reinstalling SQLAlchemy:")
            if result.stderr:
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error fixing SQLAlchemy: {e}")
        return False

if __name__ == "__main__":
    print("SQLAlchemy Check and Fix")
    print("=" * 30)
    
    if check_sqlalchemy():
        print("\n🎉 SQLAlchemy is working correctly!")
    else:
        print("\nAttempting to fix SQLAlchemy...")
        if fix_sqlalchemy():
            print("Retrying SQLAlchemy check...")
            if check_sqlalchemy():
                print("\n🎉 SQLAlchemy is now working correctly!")
            else:
                print("\n💥 SQLAlchemy is still not working.")
        else:
            print("\n💥 Failed to fix SQLAlchemy.")
            
    print("\n💡 If issues persist, try:")
    print("   pip install sqlalchemy==2.0.23 --force-reinstall")