# AI App Builder - Verification Tools

This document explains how to use the verification tools to check if your AI App Builder services are running correctly.

## Backend Verification

### Option 1: Using the Python script directly
From the `backend` directory:
```bash
python VERIFY_BACKEND.py
```

### Option 2: Using the batch file
From the `backend` directory:
```bash
VERIFY_BACKEND.bat
```

Or double-click on `VERIFY_BACKEND.bat` in Windows Explorer.

## Frontend Verification

### Option 1: Using the Node.js script directly
From the `frontend` directory:
```bash
node VERIFY_FRONTEND.js
```

### Option 2: Using the batch file
From the `frontend` directory:
```bash
VERIFY_FRONTEND.bat
```

Or double-click on `VERIFY_FRONTEND.bat` in Windows Explorer.

## What Each Tool Checks

### Backend Verification (`VERIFY_BACKEND.py`)
- Checks if the backend server is running on port 8000
- Verifies the root endpoint (`/`) is responding correctly
- Checks the health endpoint (`/health`) for database status
- Provides clear feedback on any issues found

### Frontend Verification (`VERIFY_FRONTEND.js`)
- Checks if the frontend server is running on port 3000
- Verifies basic connectivity to the frontend service
- Provides clear feedback on any issues found

## Common Issues and Solutions

### "Module not found" errors
If you see errors about missing modules:

For backend:
```bash
pip install requests
```

For frontend:
Make sure you have Node.js installed on your system.

### "Connection refused" errors
This usually means the service is not running. Make sure to start the services:

For backend:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

For frontend:
```bash
npm start
```

## Access URLs

After verification, if services are running correctly:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Important Notes

1. **Never use `http://0.0.0.0:8000`** in your browser - it won't work
2. **Always use `http://localhost:8000`** for backend access
3. **Always use `http://localhost:3000`** for frontend access
4. Keep both terminal windows open while using the application
5. The first startup of the frontend may take 1-2 minutes due to compilation