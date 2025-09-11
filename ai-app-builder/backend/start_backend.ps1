# start_backend.ps1
Write-Host "Starting AI App Builder Backend Server..." -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host "Server Address: http://localhost:8000" -ForegroundColor Yellow
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "IMPORTANT: Use http://localhost:8000 in your browser, NOT 0.0.0.0" -ForegroundColor Cyan
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Gray
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

Set-Location -Path "c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload