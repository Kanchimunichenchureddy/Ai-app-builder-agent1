# PowerShell script to start both backend and frontend
Write-Host "========================================" -ForegroundColor Green
Write-Host "  AI APP BUILDER - START APPLICATION" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "This script will help you start both the backend and frontend." -ForegroundColor Cyan
Write-Host ""
Write-Host "INSTRUCTIONS:" -ForegroundColor Yellow
Write-Host "1. This will open two new terminal windows" -ForegroundColor Gray
Write-Host "2. Leave both windows open while using the application" -ForegroundColor Gray
Write-Host "3. Backend will run on: http://localhost:8000" -ForegroundColor Gray
Write-Host "4. Frontend will run on: http://localhost:3000" -ForegroundColor Gray
Write-Host "5. Press any key to continue..." -ForegroundColor Gray
Write-Host ""
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Get the base directory
$baseDir = "C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder"

Write-Host "Starting Backend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$baseDir\backend'; Write-Host 'Starting Backend Server...' -ForegroundColor Green; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

Start-Sleep -Seconds 5

Write-Host "Starting Frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$baseDir\frontend'; Write-Host 'Starting Frontend...' -ForegroundColor Green; npm start"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  APPLICATION STARTED SUCCESSFULLY" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "ACCESS POINTS:" -ForegroundColor Yellow
Write-Host " Backend API:     http://localhost:8000" -ForegroundColor Gray
Write-Host " Backend Docs:    http://localhost:8000/docs" -ForegroundColor Gray
Write-Host " Frontend App:    http://localhost:3000" -ForegroundColor Gray
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host " - Keep both terminal windows open" -ForegroundColor Gray
Write-Host " - The frontend may take 1-2 minutes to compile" -ForegroundColor Gray
Write-Host " - If you see connection errors, wait for both servers to fully start" -ForegroundColor Gray
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")