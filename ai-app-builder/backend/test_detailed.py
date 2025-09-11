import sys
import os
import traceback

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

def test_imports():
    """Test imports to identify where the issue occurs."""
    print("Testing imports...")
    
    try:
        print("1. Importing database module...")
        from app.core.database import init_database, get_db
        print("   Database module imported successfully")
        
        print("2. Importing security module...")
        from app.core.security import create_access_token, verify_token, get_password_hash, verify_password
        print("   Security module imported successfully")
        
        print("3. Importing User model...")
        from app.models.user import User
        print("   User model imported successfully")
        
        print("4. Importing Project model...")
        from app.models.project import Project
        print("   Project model imported successfully")
        
        print("5. Importing Deployment model...")
        from app.models.deployment import Deployment
        print("   Deployment model imported successfully")
        
        return True
    except Exception as e:
        print(f"Import test failed: {e}")
        traceback.print_exc()
        return False

def test_database_init():
    """Test database initialization."""
    print("\nTesting database initialization...")
    
    try:
        from app.core.database import init_database
        result = init_database()
        print(f"Database initialization result: {result}")
        return True
    except Exception as e:
        print(f"Database initialization failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running detailed tests...")
    
    success = True
    success &= test_imports()
    success &= test_database_init()
    
    if success:
        print("\nAll detailed tests passed!")
    else:
        print("\nSome detailed tests failed!")
        sys.exit(1)