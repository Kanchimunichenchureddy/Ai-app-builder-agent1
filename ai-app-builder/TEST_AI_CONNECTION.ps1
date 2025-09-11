# PowerShell script to test AI connection
Write-Host "========================================" -ForegroundColor Green
Write-Host "  AI App Builder - Connection Test" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Testing connection between frontend and backend for AI chat functionality..." -ForegroundColor Cyan
Write-Host ""

python TEST_AI_CONNECTION.py

Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null