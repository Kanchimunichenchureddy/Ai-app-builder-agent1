import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Python version:", sys.version)
print("Python path:", sys.path[:3])

try:
    import sqlalchemy
    print("SQLAlchemy imported successfully")
    print("SQLAlchemy version:", sqlalchemy.__version__)
except Exception as e:
    print("Failed to import SQLAlchemy:", e)

try:
    from app.main import app
    print("Main app imported successfully")
except Exception as e:
    print("Failed to import main app:", e)
    import traceback
    traceback.print_exc()