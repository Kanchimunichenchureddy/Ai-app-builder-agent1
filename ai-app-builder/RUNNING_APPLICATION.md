# Running Application Guide

## Current Status

1. **Backend Server**: ✅ RUNNING on port 8001
   - API Base URL: http://localhost:8001/api
   - API Documentation: http://localhost:8001/docs
   - Health Check: http://localhost:8001/health

2. **Frontend Server**: ⚠️ NEEDS MANUAL START on port 3001

## Accessing the Backend

The backend server is already running and accessible. You can verify this by:

1. Opening your browser and navigating to:
   - http://localhost:8001/ - Should show welcome message
   - http://localhost:8001/health - Should show health status
   - http://localhost:8001/docs - Should show API documentation

2. Or using PowerShell commands:
   ```powershell
   Invoke-WebRequest -Uri http://localhost:8001/ -Method GET
   Invoke-WebRequest -Uri http://localhost:8001/health -Method GET
   ```

## Starting the Frontend Server

To start the frontend server, follow these steps:

### Method 1: Using Command Line (Recommended)
1. Open a new PowerShell terminal
2. Navigate to the frontend directory:
   ```powershell
   cd "c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\frontend"
   ```
3. Set the PORT environment variable:
   ```powershell
   $env:PORT=3001
   ```
4. Start the frontend:
   ```powershell
   npx react-scripts start
   ```
5. When prompted with "Need to install the following packages: react-scripts@5.0.1 Ok to proceed? (y)", type `y` and press Enter

### Method 2: Using the Batch File
1. Double-click on the file:
   ```
   c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\frontend\start_frontend_proper.bat
   ```

### Method 3: Using Node.js Script
1. Open a PowerShell terminal
2. Run the Node.js script:
   ```powershell
   node "c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\frontend\start_frontend.js"
   ```

## Accessing the Full Application

Once both servers are running:

- **Frontend Application**: http://localhost:3001
- **Backend API**: http://localhost:8001/api
- **API Documentation**: http://localhost:8001/docs

## Troubleshooting

1. **If you get "port already in use" errors:**
   - Kill the processes using those ports:
     ```powershell
     netstat -ano | findstr :8001
     Stop-Process -Id [PROCESS_ID] -Force
     ```
   - Or change the port in the startup scripts

2. **If you get CORS errors:**
   - Make sure both frontend and backend servers are running
   - Check that the CORS settings in the backend match the frontend URL

3. **If the frontend fails to start:**
   - Make sure Node.js and npm are installed
   - Try running `npm install` in the frontend directory first

4. **If you can't navigate to the frontend directory:**
   - Use the full path in quotes:
     ```powershell
     cd "c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\frontend"
     ```

## Testing the Connection

You can test the connection between frontend and backend by opening the test file:
```
c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\TEST_CONNECTION.html
```

This will verify that the frontend can communicate with the backend.