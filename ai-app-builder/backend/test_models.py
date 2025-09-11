import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

def test_model_imports():
    """Test importing models to check for circular import issues."""
    print("Testing model imports...")
    
    try:
        print("1. Importing database module...")
        from app.core.database import init_database
        print("   Database module imported successfully")
        
        print("2. Initializing database...")
        init_database()
        print("   Database initialized successfully")
        
        print("3. Importing User model...")
        from app.models.user import User
        print("   User model imported successfully")
        
        print("4. Importing Project model...")
        from app.models.project import Project
        print("   Project model imported successfully")
        
        print("5. Importing Deployment model...")
        from app.models.deployment import Deployment
        print("   Deployment model imported successfully")
        
        print("6. Testing database session...")
        from app.core.database import get_db
        db_gen = get_db()
        db = next(db_gen)
        print("   Database session created successfully")
        
        # Close session
        try:
            next(db_gen)
        except StopIteration:
            pass
        
        return True
    except Exception as e:
        print(f"Model import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running model import tests...")
    
    success = test_model_imports()
    
    if success:
        print("\nAll model import tests passed!")
    else:
        print("\nModel import tests failed!")
        sys.exit(1)