@echo off
title AI App Builder - Launcher
color 0A

echo =====================================================================
echo                    AI APP BUILDER LAUNCHER
echo =====================================================================
echo.
echo This script will help you start the AI App Builder application.
echo.
echo The application consists of two parts:
echo   1. Backend API server (runs on port 8000)
echo   2. Frontend web application (runs on port 3000)
echo.
echo After starting, you can access:
echo   Frontend: http://localhost:3000
echo   Backend: http://localhost:8000
echo   Docs:    http://localhost:8000/docs
echo.
echo IMPORTANT: Do NOT use http://0.0.0.0:8000 in your browser!
echo            Always use http://localhost:8000 instead.
echo.
echo Press any key to start the application...
pause >nul

cls
echo =====================================================================
echo                    STARTING BACKEND SERVER
echo =====================================================================
echo.
echo The backend server will start in a new window.
echo Please wait for the "Application startup complete" message.
echo.
echo DO NOT close the backend window while using the application.
echo.

REM Start backend in a new minimized window
start "Backend Server - Minimized" /min cmd /c "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload && pause"

echo Waiting 10 seconds for backend to start...
timeout /t 10 /nobreak >nul

cls
echo =====================================================================
echo                    STARTING FRONTEND APPLICATION
echo =====================================================================
echo.
echo The frontend application will start in a new window.
echo Please wait for the "webpack compiled successfully" message.
echo This may take 1-2 minutes on the first run.
echo.
echo DO NOT close the frontend window while using the application.
echo.

REM Start frontend in a new minimized window
start "Frontend App - Minimized" /min cmd /c "cd frontend && npm start && pause"

echo Waiting 15 seconds for frontend to start...
timeout /t 15 /nobreak >nul

cls
echo =====================================================================
echo                    APPLICATION STARTED SUCCESSFULLY
echo =====================================================================
echo.
echo 🎉 The AI App Builder application has been started!
echo.
echo ACCESS URLS:
echo   Frontend Application: http://localhost:3000
echo   Backend API:          http://localhost:8000
echo   API Documentation:    http://localhost:8000/docs
echo.
echo TROUBLESHOOTING:
echo   1. If pages don't load, wait a bit longer for compilation
echo   2. Check that both command windows are still open
echo   3. If issues persist, close both windows and run this script again
echo.
echo VERIFICATION:
echo   Open VERIFY_CONNECTION.html in your browser to test the connection
echo.
echo Press any key to open the frontend in your default browser...
pause >nul

REM Open the frontend in the default browser
start http://localhost:3000

echo.
echo Application started! Check your browser.
echo.
echo Press any key to close this window...
pause >nul