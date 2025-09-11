# PowerShell script to automatically install missing dependencies
Write-Host "========================================" -ForegroundColor Green
Write-Host "  AI App Builder - Auto Install Dependencies" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Installing missing dependencies..." -ForegroundColor Cyan
Write-Host ""

# Install the missing packages
pip install python-multipart python-jose[cryptography] python-dotenv pydantic-settings gitpython

Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Cyan
Write-Host ""

# Run the dependency check
python CHECK_DEPENDENCIES.py

Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null