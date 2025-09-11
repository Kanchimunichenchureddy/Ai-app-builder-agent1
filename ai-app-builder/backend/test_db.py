import os
import sys
from app.core.config import settings

print("Testing database connection...")
print(f"DATABASE_URL: {settings.DATABASE_URL}")

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    # Create engine
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=True
    )
    
    # Test connection
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print("Database connection successful!")
        print(f"Result: {result.fetchone()}")
        
except Exception as e:
    print(f"Database connection failed: {e}")
    print(f"Error type: {type(e).__name__}")