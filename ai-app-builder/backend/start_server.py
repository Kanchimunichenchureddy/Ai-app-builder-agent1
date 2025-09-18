import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import and run the FastAPI app
import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)