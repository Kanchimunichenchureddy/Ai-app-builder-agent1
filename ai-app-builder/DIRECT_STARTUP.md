# AI App Builder - Direct Startup Guide

This guide will help you run the AI App Builder directly without Docker.

## Prerequisites

1. Python 3.8 or higher
2. Node.js 14 or higher
3. MySQL 8.0 or higher (optional, for full functionality)

## Setup Instructions

### 1. Database Setup (Optional but Recommended)

Run the database initialization script:
```
backend\init_db.bat
```

This will provide instructions for setting up the MySQL database.

### 2. Backend Setup

Navigate to the backend directory and run:
```
cd backend
run_backend.bat
```

This script will:
- Create a Python virtual environment
- Install all required dependencies
- Create a .env file from .env.example
- Start the FastAPI backend server

### 3. Frontend Setup

Navigate to the frontend directory and run:
```
cd frontend
run_frontend.bat
```

This script will:
- Install all required Node.js dependencies
- Create a .env file from .env.example
- Start the React frontend server

### 4. Run Both Services

From the main directory, you can run:
```
start_direct.bat
```

This will start both the backend and frontend services.

## Accessing the Application

Once both services are running:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Configuration

### Backend Configuration

Edit `backend/.env` to configure:
- Database connection
- AI service API keys (OpenAI, Gemini, DeepSeek)
- Security settings
- Stripe integration (for payment features)

### Frontend Configuration

Edit `frontend/.env` to configure:
- API endpoint URL

## Troubleshooting

### Common Issues

1. **Port already in use**: If port 8000 or 3000 is already in use, the servers will fail to start.
   - Solution: Stop the processes using those ports or modify the startup scripts to use different ports.

2. **Missing dependencies**: If you see import errors, dependencies may not have installed correctly.
   - Solution: Run `pip install -r requirements.txt` in the backend directory.

3. **Database connection failed**: If you skipped database setup, some features will be limited.
   - Solution: Run the database initialization script.

### API Keys

To use AI features, you need to configure at least one of these API keys in `backend/.env`:

- OPENAI_API_KEY
- GEMINI_API_KEY
- DEEPSEEK_API_KEY

## Features

The AI App Builder includes:

1. **AI Chat Interface** - Chat with an AI assistant to build applications
2. **Project Builder** - Generate complete applications from natural language descriptions
3. **Code Generation** - Generate code for specific components
4. **Project Management** - Manage your generated projects
5. **Deployment** - Deploy applications to various platforms
6. **Integrations** - Connect with external services like Stripe, Google APIs

## Support

For issues with the direct startup method, please check:
1. That all prerequisites are installed
2. That ports 8000 and 3000 are available
3. The error messages in the terminal windows