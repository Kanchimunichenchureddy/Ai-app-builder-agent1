# PowerShell script to launch the AI App Builder application
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "                   AI APP BUILDER LAUNCHER" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "This script will help you start the AI App Builder application." -ForegroundColor Cyan
Write-Host ""
Write-Host "The application consists of two parts:" -ForegroundColor Yellow
Write-Host "  1. Backend API server (runs on port 8000)" -ForegroundColor Gray
Write-Host "  2. Frontend web application (runs on port 3000)" -ForegroundColor Gray
Write-Host ""
Write-Host "After starting, you can access:" -ForegroundColor Yellow
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Gray
Write-Host "  Backend: http://localhost:8000" -ForegroundColor Gray
Write-Host "  Docs:    http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "IMPORTANT: Do NOT use http://0.0.0.0:8000 in your browser!" -ForegroundColor Red
Write-Host "           Always use http://localhost:8000 instead." -ForegroundColor Red
Write-Host ""
Write-Host "Press any key to start the application..." -ForegroundColor Cyan
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null

Clear-Host
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "                   STARTING BACKEND SERVER" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "The backend server will start in a new window." -ForegroundColor Cyan
Write-Host "Please wait for the `"Application startup complete`" message." -ForegroundColor Cyan
Write-Host ""
Write-Host "DO NOT close the backend window while using the application." -ForegroundColor Yellow
Write-Host ""

# Start backend in a new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PWD\backend'; Write-Host 'Starting Backend Server...' -ForegroundColor Green; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

Write-Host "Waiting 10 seconds for backend to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

Clear-Host
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "                   STARTING FRONTEND APPLICATION" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "The frontend application will start in a new window." -ForegroundColor Cyan
Write-Host "Please wait for the `"webpack compiled successfully`" message." -ForegroundColor Cyan
Write-Host "This may take 1-2 minutes on the first run." -ForegroundColor Cyan
Write-Host ""
Write-Host "DO NOT close the frontend window while using the application." -ForegroundColor Yellow
Write-Host ""

# Start frontend in a new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PWD\frontend'; Write-Host 'Starting Frontend Application...' -ForegroundColor Green; npm start"

Write-Host "Waiting 15 seconds for frontend to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 15

Clear-Host
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "                   APPLICATION STARTED SUCCESSFULLY" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 The AI App Builder application has been started!" -ForegroundColor Green
Write-Host ""
Write-Host "ACCESS URLS:" -ForegroundColor Yellow
Write-Host "  Frontend Application: http://localhost:3000" -ForegroundColor Gray
Write-Host "  Backend API:          http://localhost:8000" -ForegroundColor Gray
Write-Host "  API Documentation:    http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "TROUBLESHOOTING:" -ForegroundColor Yellow
Write-Host "  1. If pages don't load, wait a bit longer for compilation" -ForegroundColor Gray
Write-Host "  2. Check that both PowerShell windows are still open" -ForegroundColor Gray
Write-Host "  3. If issues persist, close both windows and run this script again" -ForegroundColor Gray
Write-Host ""
Write-Host "VERIFICATION:" -ForegroundColor Yellow
Write-Host "  Open VERIFY_CONNECTION.html in your browser to test the connection" -ForegroundColor Gray
Write-Host ""
Write-Host "Press any key to open the frontend in your default browser..." -ForegroundColor Cyan
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null

# Open the frontend in the default browser
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "Application started! Check your browser." -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Cyan
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null