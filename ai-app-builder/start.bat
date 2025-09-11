@echo off
echo Starting AI App Builder...
echo ======================================

echo Starting Backend Server
echo ----------------------
echo The backend server will start on port 8000
echo IMPORTANT: Access the backend at http://localhost:8000 (NOT 0.0.0.0)
echo API Documentation: http://localhost:8000/docs
echo.

cd backend
start "Backend Server" /D "%CD%" cmd /c "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
cd ..

timeout /t 5 /nobreak >nul

echo Starting Frontend Server
echo -----------------------
echo The frontend server will start on port 3000
echo Application URL: http://localhost:3000
echo.

cd frontend
start "Frontend Server" /D "%CD%" cmd /c "npm start"
cd ..

echo ======================================
echo Both servers are now starting...
echo.
echo BACKEND:  http://localhost:8000
echo FRONTEND: http://localhost:3000
echo API DOCS: http://localhost:8000/docs
echo ======================================
echo.
echo Press any key to close this window...
pause >nul