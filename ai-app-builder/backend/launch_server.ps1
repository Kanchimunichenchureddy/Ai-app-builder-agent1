# Simple PowerShell script to launch the server
Set-Location -Path "C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload