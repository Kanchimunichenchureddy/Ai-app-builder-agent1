@echo off
cd /d "c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend"
echo Starting AI App Builder Backend...
echo =================================
echo Make sure you have activated your virtual environment
echo =================================
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause