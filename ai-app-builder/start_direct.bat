@echo off
echo AI App Builder - Direct Startup
echo ===============================
echo.

REM Check if we're in the right directory
if not exist backend (
    echo Error: backend directory not found!
    echo Please run this script from the ai-app-builder directory.
    pause
    exit /b 1
)

echo 1. Initializing database setup...
echo ==============================
call backend\init_db.bat

echo.
echo 2. Starting backend server...
echo ===========================
start "Backend Server" /D "backend" run_backend.bat

echo.
echo 3. Starting frontend server...
echo =============================
start "Frontend Server" /D "frontend" run_frontend.bat

echo.
echo Servers starting up...
echo.
echo Backend API will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000
echo API Documentation: http://localhost:8000/docs
echo.
echo Please wait for both servers to start completely.
echo.
echo Press any key to continue...
pause