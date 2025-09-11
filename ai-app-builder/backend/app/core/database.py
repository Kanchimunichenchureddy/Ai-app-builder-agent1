from .config import settings
import os

# Global variables for engine, SessionLocal, and Base
engine = None
SessionLocal = None
Base = None
metadata = None

def init_database():
    """Initialize database components with lazy loading to avoid import issues"""
    global engine, SessionLocal, Base, metadata
    
    try:
        # Import SQLAlchemy components only when needed
        from sqlalchemy import create_engine, MetaData
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker
        
        # Determine database URL with fallback
        def get_database_url():
            try:
                # Try to use the configured database URL
                db_url = settings.DATABASE_URL
                print(f"Attempting to connect to database: {db_url}")
                
                # Test if we can import the required database driver
                if db_url.startswith("mysql"):
                    import pymysql
                elif db_url.startswith("sqlite"):
                    pass  # sqlite3 is built into Python
                elif db_url.startswith("postgresql"):
                    import psycopg2
                
                return db_url
            except ImportError as e:
                print(f"Database driver not available: {e}")
                print("Falling back to SQLite database")
                return "sqlite:///./test.db"
            except Exception as e:
                print(f"Error determining database URL: {e}")
                print("Falling back to SQLite database")
                return "sqlite:///./test.db"

        # Create SQLAlchemy engine
        try:
            DATABASE_URL = get_database_url()
            engine = create_engine(
                DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=settings.DEBUG
            )
            print(f"Database engine created with URL: {DATABASE_URL}")
        except Exception as e:
            print(f"Failed to create database engine: {e}")
            # Fallback to SQLite
            DATABASE_URL = "sqlite:///./fallback.db"
            engine = create_engine(
                DATABASE_URL,
                pool_pre_ping=True,
                echo=settings.DEBUG
            )
            print(f"Fallback database engine created with URL: {DATABASE_URL}")

        # Create SessionLocal class
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        # Create Base class
        Base = declarative_base()

        # Metadata
        metadata = MetaData()
        
        return True
    except Exception as e:
        print(f"Failed to initialize database components: {e}")
        return False

# Initialize database components
db_initialized = init_database()

# Dependency to get database session
def get_db():
    if not db_initialized or SessionLocal is None:
        # Return a mock session if database is not initialized
        class MockSession:
            def execute(self, query):
                return None
            def close(self):
                pass
        yield MockSession()
        return
        
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
def create_tables():
    if not db_initialized or Base is None or engine is None:
        print("Database not initialized, skipping table creation")
        return
        
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Failed to create database tables: {e}")
        # Try with SQLite as last resort
        try:
            print("Trying with SQLite fallback...")
            from sqlalchemy import create_engine
            fallback_engine = create_engine("sqlite:///./fallback_tables.db", echo=settings.DEBUG)
            Base.metadata.create_all(bind=fallback_engine)
            print("Database tables created successfully with SQLite fallback")
        except Exception as fallback_e:
            print(f"Fallback also failed: {fallback_e}")
