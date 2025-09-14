# OpenRouter API Key Verification Script
Set-Location -Path "C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend"

Write-Host "🚀 Verifying OpenRouter API Key..." -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""

python verify_openrouter_key.py

Write-Host ""
Write-Host "Press any key to exit..."
$host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")