# PowerShell script to fix Google authentication package import issues

Write-Host "🔧 Fixing Google authentication package import issues..." -ForegroundColor Green

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

# Google packages that need to be fixed
$googlePackages = @(
    @{Name="google-auth-oauthlib"; Version="1.1.0"},
    @{Name="google-auth-httplib2"; Version="0.1.1"},
    @{Name="google-api-python-client"; Version="2.108.0"}
)

$failedPackages = @()

foreach ($package in $googlePackages) {
    Write-Host "`n🔧 Fixing $($package.Name)..." -ForegroundColor Cyan
    
    # First, uninstall the package
    Write-Host "🗑️  Uninstalling $($package.Name)..." -ForegroundColor Yellow
    try {
        & $pipPath uninstall $package.Name -y
        Write-Host "✅ Uninstall command completed" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Could not uninstall $($package.Name): $_" -ForegroundColor Yellow
    }
    
    # Try multiple installation approaches
    $installApproaches = @(
        "$($package.Name)==$($package.Version) --force-reinstall --no-cache-dir",
        "$($package.Name)==$($package.Version) --force-reinstall",
        "$($package.Name) --force-reinstall --no-cache-dir",
        "$($package.Name) --force-reinstall"
    )
    
    $installed = $false
    for ($i = 0; $i -lt $installApproaches.Count; $i++) {
        $installCmd = $installApproaches[$i]
        Write-Host "Attempt $($i+1): $installCmd" -ForegroundColor Yellow
        try {
            & $pipPath install $installCmd
            Write-Host "✅ $($package.Name) installed successfully!" -ForegroundColor Green
            $installed = $true
            break
        } catch {
            Write-Host "❌ Attempt $($i+1) failed: $_" -ForegroundColor Red
        }
    }
    
    if (-not $installed) {
        $failedPackages += "$($package.Name)==$($package.Version)"
        continue
    }
    
    # Test the import
    Write-Host "🧪 Testing $($package.Name) import..." -ForegroundColor Yellow
    try {
        switch ($package.Name) {
            "google-auth-oauthlib" {
                python -c "import google.auth.oauthlib; print('✅ google-auth-oauthlib import successful!')"
            }
            "google-auth-httplib2" {
                python -c "import google_auth_httplib2; print('✅ google-auth-httplib2 import successful!')"
            }
            "google-api-python-client" {
                python -c "import googleapiclient; print('✅ google-api-python-client import successful!')"
            }
        }
    } catch {
        Write-Host "❌ $($package.Name) import failed: $_" -ForegroundColor Red
        $failedPackages += "$($package.Name)==$($package.Version)"
    }
}

# Summary
if ($failedPackages.Count -gt 0) {
    Write-Host "`n❌ Failed to fix $($failedPackages.Count) packages:" -ForegroundColor Red
    foreach ($failed in $failedPackages) {
        Write-Host "   - $failed" -ForegroundColor Red
    }
    exit 1
} else {
    Write-Host "`n🎉 All Google packages fixed successfully!" -ForegroundColor Green
    exit 0
}