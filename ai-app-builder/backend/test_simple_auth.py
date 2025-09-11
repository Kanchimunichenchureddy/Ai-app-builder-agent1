import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from app.core.database import init_database, get_db
from app.core.security import create_access_token, verify_token, get_password_hash
from app.models.user import User

def test_simple_auth():
    """Test simple authentication flow."""
    print("Testing simple authentication flow...")
    
    try:
        # Initialize database
        print("1. Initializing database...")
        db_initialized = init_database()
        print(f"   Database initialized: {db_initialized}")
        
        if not db_initialized:
            print("   Failed to initialize database")
            return False
        
        # Get database session
        print("2. Getting database session...")
        db_gen = get_db()
        db = next(db_gen)
        print("   Database session created")
        
        # Check if we have a user
        print("3. Checking for existing user...")
        user = db.query(User).first()
        if user:
            print(f"   Found user: {user.email} (ID: {user.id})")
        else:
            print("   No users found")
        
        # Close session
        try:
            next(db_gen)
        except StopIteration:
            pass
        
        # Test token creation
        print("4. Testing token creation...")
        token_data = {"sub": 1, "email": "test@example.com"}
        token = create_access_token(token_data)
        print(f"   Token created: {token[:20]}...")
        
        # Test token verification
        print("5. Testing token verification...")
        payload = verify_token(token)
        print(f"   Token verified: {payload}")
        
        return True
    except Exception as e:
        print(f"Simple authentication test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running simple authentication test...")
    
    success = test_simple_auth()
    
    if success:
        print("\nSimple authentication test passed!")
    else:
        print("\nSimple authentication test failed!")
        sys.exit(1)