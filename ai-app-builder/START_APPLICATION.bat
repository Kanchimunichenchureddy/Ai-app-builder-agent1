@echo off
title AI App Builder - Start Script
color 0A

echo ========================================
echo   AI APP BUILDER - START APPLICATION
echo ========================================
echo.
echo This script will help you start both the backend and frontend.
echo.
echo INSTRUCTIONS:
echo 1. This will open two new command windows
echo 2. Leave both windows open while using the application
echo 3. Backend will run on: http://localhost:8000
echo 4. Frontend will run on: http://localhost:3000
echo 5. Press any key to continue...
echo.
pause

echo Starting Backend Server...
start "Backend Server" cmd /k "cd /d C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 5 /nobreak >nul

echo Starting Frontend...
start "Frontend App" cmd /k "cd /d C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\frontend && npm start"

echo.
echo ========================================
echo   APPLICATION STARTED SUCCESSFULLY
echo ========================================
echo.
echo ACCESS POINTS:
echo  Backend API:     http://localhost:8000
echo  Backend Docs:    http://localhost:8000/docs
echo  Frontend App:    http://localhost:3000
echo.
echo IMPORTANT:
echo  - Keep both command windows open
echo  - The frontend may take 1-2 minutes to compile
echo  - If you see connection errors, wait for both servers to fully start
echo.
echo Press any key to close this window...
pause >nul