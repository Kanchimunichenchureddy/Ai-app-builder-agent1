import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from app.core.database import init_database, get_db
from app.core.security import create_access_token, verify_token, get_password_hash, verify_password
from app.models.user import User
from sqlalchemy.orm import Session

def test_database_models():
    """Test database models initialization."""
    print("Testing database models...")
    
    try:
        # Initialize database
        db_initialized = init_database()
        print(f"Database initialized: {db_initialized}")
        
        if not db_initialized:
            print("Failed to initialize database")
            return False
        
        # Try to import models after database initialization
        from app.models.user import User
        from app.models.project import Project
        from app.models.deployment import Deployment
        
        print("Models imported successfully")
        return True
    except Exception as e:
        print(f"Database models test failed: {e}")
        return False

def test_user_creation():
    """Test user creation in database."""
    print("\nTesting user creation...")
    
    try:
        # Initialize database
        init_database()
        
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
        
        # Check if test user already exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("Test user already exists")
            # Close session
            try:
                next(db_gen)
            except StopIteration:
                pass
            return True
        
        # Create a test user
        hashed_password = get_password_hash("testpassword")
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=hashed_password,
            full_name="Test User"
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"User created successfully: {test_user.email} (ID: {test_user.id})")
        
        # Close session
        try:
            next(db_gen)
        except StopIteration:
            pass
            
        return True
    except Exception as e:
        print(f"User creation test failed: {e}")
        return False

def test_user_authentication():
    """Test user authentication flow."""
    print("\nTesting user authentication...")
    
    try:
        # Initialize database
        init_database()
        
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
        
        # Find test user
        user = db.query(User).filter(User.email == "test@example.com").first()
        if not user:
            print("Test user not found")
            # Close session
            try:
                next(db_gen)
            except StopIteration:
                pass
            return False
        
        # Verify password
        password_valid = verify_password("testpassword", user.hashed_password)
        print(f"Password verification: {password_valid}")
        
        # Create JWT token
        token_data = {"sub": user.id, "email": user.email}
        token = create_access_token(token_data)
        print(f"Token created: {token[:20]}...")
        
        # Verify token
        payload = verify_token(token)
        print(f"Token payload: {payload}")
        
        # Close session
        try:
            next(db_gen)
        except StopIteration:
            pass
            
        return True
    except Exception as e:
        print(f"User authentication test failed: {e}")
        return False

if __name__ == "__main__":
    print("Running comprehensive authentication flow tests...")
    
    success = True
    success &= test_database_models()
    success &= test_user_creation()
    success &= test_user_authentication()
    
    if success:
        print("\nAll authentication flow tests passed!")
    else:
        print("\nSome authentication flow tests failed!")
        sys.exit(1)