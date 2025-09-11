import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from app.core.database import init_database, get_db
from app.core.security import create_access_token, verify_token
from app.models.user import User
from sqlalchemy.orm import Session

def test_database_connection():
    """Test database connection and initialization."""
    print("Testing database connection...")
    
    # Initialize database
    db_initialized = init_database()
    print(f"Database initialized: {db_initialized}")
    
    if not db_initialized:
        print("Failed to initialize database")
        return False
    
    # Try to get a database session
    try:
        db_gen = get_db()
        db = next(db_gen)
        print("Database session created successfully")
        
        # Test a simple query
        result = db.query(User).first()
        print(f"Database query test: {result}")
        
        # Close the session
        try:
            next(db_gen)  # This should raise StopIteration
        except StopIteration:
            pass
            
        return True
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False

def test_token_creation_and_verification():
    """Test JWT token creation and verification."""
    print("\nTesting token creation and verification...")
    
    # Test data
    user_data = {"sub": 1, "email": "test@example.com"}
    
    # Create token
    try:
        token = create_access_token(user_data)
        print(f"Token created successfully: {token[:20]}...")
    except Exception as e:
        print(f"Token creation failed: {e}")
        return False
    
    # Verify token
    try:
        payload = verify_token(token)
        print(f"Token verified successfully: {payload}")
        return True
    except Exception as e:
        print(f"Token verification failed: {e}")
        return False

def test_user_lookup():
    """Test user lookup in database."""
    print("\nTesting user lookup...")
    
    try:
        # Initialize database
        init_database()
        
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
        
        # Try to find a user
        user = db.query(User).first()
        if user:
            print(f"Found user: {user.email} (ID: {user.id})")
        else:
            print("No users found in database")
            
        # Close session
        try:
            next(db_gen)
        except StopIteration:
            pass
            
        return True
    except Exception as e:
        print(f"User lookup failed: {e}")
        return False

if __name__ == "__main__":
    print("Running authentication tests...")
    
    success = True
    success &= test_database_connection()
    success &= test_token_creation_and_verification()
    success &= test_user_lookup()
    
    if success:
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed!")
        sys.exit(1)