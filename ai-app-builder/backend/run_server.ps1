Set-Location -Path "C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend"
Write-Host "Starting AI App Builder Backend Server..."
Write-Host "Server will be available at http://localhost:8000"
Write-Host "Press Ctrl+C to stop the server"
Write-Host ""
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload