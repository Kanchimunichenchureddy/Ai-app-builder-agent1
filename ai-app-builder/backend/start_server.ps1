# PowerShell script to start the AI App Builder backend server
Write-Host "🚀 Starting AI App Builder Backend Server..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Server will be available at:" -ForegroundColor Cyan
Write-Host "  http://localhost:8000" -ForegroundColor Yellow
Write-Host "  http://localhost:8000/docs (API Documentation)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Change to the backend directory
Set-Location -Path "C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend"

# Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload