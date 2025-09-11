@echo off
title AI App Builder Backend Server
cd /d "C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend"

echo 🚀 Starting AI App Builder Backend Server...
echo ========================================
echo.
echo Server will be available at:
echo   http://localhost:8000
echo   http://localhost:8000/docs (API Documentation)
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause