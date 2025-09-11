# PowerShell script to install all dependencies
Write-Host "========================================" -ForegroundColor Green
Write-Host "  AI App Builder - Install All Dependencies" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Installing all dependencies from requirements.txt..." -ForegroundColor Cyan
Write-Host ""

# Install all dependencies from requirements.txt
pip install -r requirements.txt

Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Cyan
Write-Host ""

# Run the dependency check
python CHECK_DEPENDENCIES.py

Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null