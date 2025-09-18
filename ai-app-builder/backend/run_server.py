import os
import sys
import uvicorn
from app.main import app

if __name__ == "__main__":
    # Change to the backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    # Add the backend directory to Python path
    sys.path.insert(0, backend_dir)
    
    print(f"Starting server in directory: {backend_dir}")
    print("Server will be available at: http://localhost:8000")
    
    # Run the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )