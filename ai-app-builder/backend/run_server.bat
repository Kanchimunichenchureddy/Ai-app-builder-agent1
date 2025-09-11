@echo off
cd /d "C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend"
echo Starting AI App Builder Backend Server...
echo Server will be available at http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause