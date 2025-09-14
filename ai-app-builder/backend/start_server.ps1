# Navigate to the backend directory
Set-Location -Path "C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend"

# Start the server
Write-Host "🚀 Starting AI App Builder Backend Server..."
Write-Host "========================================"
Write-Host ""
Write-Host "Server will be available at:"
Write-Host "  http://localhost:8000"
Write-Host "  http://localhost:8000/docs (API Documentation)"
Write-Host ""
Write-Host "Press Ctrl+C to stop the server"
Write-Host ""

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload