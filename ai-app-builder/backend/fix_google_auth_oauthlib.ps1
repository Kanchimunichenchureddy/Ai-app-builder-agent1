# PowerShell script to fix google-auth-oauthlib package import issues

Write-Host "🔧 Fixing google-auth-oauthlib package import issues..." -ForegroundColor Green

# Get the current directory
$backendDir = Get-Location
Write-Host "Working directory: $backendDir" -ForegroundColor Yellow

# Define paths
$venvPath = Join-Path $backendDir "venv"

Write-Host "Virtual environment path: $venvPath" -ForegroundColor Yellow

# Check if virtual environment exists
if (Test-Path $venvPath) {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
    $pipPath = Join-Path $venvPath "Scripts\pip.exe"
} else {
    Write-Host "⚠️  Virtual environment not found, using system pip" -ForegroundColor Yellow
    $pipPath = "pip"
}

# Check if pip exists
if (Test-Path $pipPath) {
    Write-Host "✅ Pip found at: $pipPath" -ForegroundColor Green
} else {
    Write-Host "⚠️  Pip not found at expected path, using 'pip' command" -ForegroundColor Yellow
    $pipPath = "pip"
}

# Set environment variable to disable user site-packages
$env:PYTHONNOUSERSITE = "1"
Write-Host "Disabled user site-packages" -ForegroundColor Cyan

$package = "google-auth-oauthlib"
$version = "1.2.0"  # Use the newer version

Write-Host "`n🔧 Fixing $package..." -ForegroundColor Cyan

# First, uninstall the package
Write-Host "🗑️  Uninstalling $package..." -ForegroundColor Yellow
try {
    & $pipPath uninstall $package -y
    Write-Host "✅ Uninstall command completed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not uninstall $package: $_" -ForegroundColor Yellow
}

# Try multiple installation approaches
$installApproaches = @(
    "$package==$version --force-reinstall --no-cache-dir",
    "$package==$version --force-reinstall",
    "$package --force-reinstall --no-cache-dir",
    "$package --force-reinstall",
    # Try installing without version specification
    "$package"
)

$installed = $false
for ($i = 0; $i -lt $installApproaches.Count; $i++) {
    $installCmd = $installApproaches[$i]
    Write-Host "Attempt $($i+1): $installCmd" -ForegroundColor Yellow
    try {
        & $pipPath install $installCmd
        Write-Host "✅ $package installed successfully!" -ForegroundColor Green
        $installed = $true
        break
    } catch {
        Write-Host "❌ Attempt $($i+1) failed: $_" -ForegroundColor Red
    }
}

if (-not $installed) {
    Write-Host "❌ Failed to install $package" -ForegroundColor Red
    exit 1
}

# Test the import
Write-Host "🧪 Testing $package import..." -ForegroundColor Yellow
try {
    python -c "import google.auth.oauthlib; print('✅ google.auth.oauthlib import successful!')"
    Write-Host "✅ $package import successful!" -ForegroundColor Green
    exit 0
} catch {
    Write-Host "❌ $package import failed: $_" -ForegroundColor Red
    # Try alternative import
    try {
        python -c "import google_auth_oauthlib; print('✅ Alternative import successful!')"
        Write-Host "✅ Alternative import successful!" -ForegroundColor Green
        exit 0
    } catch {
        Write-Host "❌ Alternative import also failed: $_" -ForegroundColor Red
        exit 1
    }
}