import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Change to the backend directory
os.chdir(backend_dir)

print(f"Working directory: {os.getcwd()}")
print(f"Python path: {sys.path[:3]}...")  # Show first few paths

# Now import and run the app
try:
    from app.main import app
    import uvicorn
    
    print("Starting server on port 8001...")
    print("Access the API at: http://localhost:8001")
    print("API Docs at: http://localhost:8001/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001  # Use port 8001 instead of 8000
    )
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()