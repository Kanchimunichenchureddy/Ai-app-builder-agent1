import sys
import os
import traceback

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from app.core.database import init_database, get_db
from app.core.security import create_access_token, verify_token, get_password_hash
from app.models.user import User
from app.api.builder import get_current_user
from fastapi.security import HTTPBearer
from fastapi import HTTPException, status

def test_chat_auth_flow():
    """Test the complete chat authentication flow."""
    print("Testing chat authentication flow...")
    
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
        if not user:
            print("   No users found, creating test user...")
            # Create a test user
            hashed_password = get_password_hash("testpassword")
            user = User(
                email="test@example.com",
                username="testuser",
                hashed_password=hashed_password,
                full_name="Test User"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"   Created user: {user.email}")
        else:
            print(f"   Found user: {user.email}")
        
        # Create a JWT token for this user
        print("4. Creating JWT token...")
        token_data = {"sub": user.id, "email": user.email}
        token = create_access_token(token_data)
        print(f"   Token created: {token[:20]}...")
        
        # Test the get_current_user function
        print("5. Testing get_current_user function...")
        try:
            # This simulates what happens in the chat endpoint
            payload = verify_token(token)
            print(f"   Token verified, payload: {payload}")
            
            if not payload:
                print("   Invalid token payload")
                return False
                
            user_id = payload.get("sub")
            if not user_id:
                print("   No user ID in token payload")
                return False
                
            # Find user in database
            db_user = db.query(User).filter(User.id == user_id).first()
            if not db_user:
                print("   User not found in database")
                return False
                
            print(f"   User authenticated: {db_user.email}")
            
        except Exception as e:
            print(f"   get_current_user failed: {e}")
            traceback.print_exc()
            return False
        finally:
            # Close database session
            try:
                next(db_gen)
            except StopIteration:
                pass
        
        return True
    except Exception as e:
        print(f"Chat authentication flow test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running chat endpoint authentication test...")
    
    success = test_chat_auth_flow()
    
    if success:
        print("\nChat endpoint authentication test passed!")
    else:
        print("\nChat endpoint authentication test failed!")
        sys.exit(1)