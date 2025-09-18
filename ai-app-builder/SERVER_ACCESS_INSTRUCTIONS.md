# Server Access Instructions

## Backend Server
The backend server is successfully running on port 8001.

- **API Base URL**: http://localhost:8001/api
- **API Documentation**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health

You can verify the backend is working by accessing these URLs in your browser:
1. http://localhost:8001/ - Should show welcome message
2. http://localhost:8001/health - Should show {"status":"healthy","database":"connected"}
3. http://localhost:8001/docs - Should show the API documentation

## Frontend Server
The frontend server needs to be started manually. Here are the steps:

### Method 1: Using Command Line
1. Open a new terminal/command prompt
2. Navigate to the frontend directory:
   ```
   cd "c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\frontend"
   ```
3. Set the PORT environment variable:
   ```
   $env:PORT=3001
   ```
4. Start the frontend:
   ```
   npx react-scripts start
   ```
5. When prompted with "Need to install the following packages: react-scripts@5.0.1 Ok to proceed? (y)", type `y` and press Enter

### Method 2: Using the Batch File
1. Double-click on the file:
   ```
   c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\frontend\start_frontend_proper.bat
   ```

## Accessing the Application
Once both servers are running:

- **Frontend Application**: http://localhost:3001
- **Backend API**: http://localhost:8001/api
- **API Documentation**: http://localhost:8001/docs

## Troubleshooting
1. If you get "port already in use" errors:
   - Kill the processes using those ports with:
     ```
     netstat -ano | findstr :8001
     Stop-Process -Id [PROCESS_ID] -Force
     ```
   - Or change the port in the startup scripts

2. If you get CORS errors:
   - Make sure both frontend and backend servers are running
   - Check that the CORS settings in the backend match the frontend URL

3. If the frontend fails to start:
   - Make sure Node.js and npm are installed
   - Try running `npm install` in the frontend directory first