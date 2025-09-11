# PowerShell script to fix package import issues for Python 3.13 compatibility

Write-Host "🔧 Fixing package import issues for Python 3.13 compatibility..." -ForegroundColor Green

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

# Packages that need to be fixed
$packagesToFix = @(
    # FastAPI and related packages with typing.Annotated issues
    @{Name="fastapi"; Version="0.104.1"},
    @{Name="openai"; Version="1.3.7"},
    @{Name="typing_extensions"; Version=$null},  # For typing compatibility
    
    # Missing packages
    @{Name="python-jose[cryptography]"; Version="3.3.0"},
    @{Name="python-dotenv"; Version="1.0.0"},
    @{Name="pydantic-settings"; Version="2.1.0"},
    @{Name="google-generativeai"; Version="0.3.2"},
    @{Name="google-auth"; Version="2.23.4"},
    # Updated to more compatible versions for Python 3.13
    @{Name="google-auth-oauthlib"; Version="1.2.0"},
    @{Name="google-auth-httplib2"; Version="0.2.0"},
    @{Name="google-api-python-client"; Version="2.110.0"}
)

$failedPackages = @()

foreach ($package in $packagesToFix) {
    $packageName = $package.Name.Split('[')[0]  # Get base package name
    Write-Host "`n🔧 Fixing $($package.Name)..." -ForegroundColor Cyan
    
    # First, uninstall the package
    Write-Host "🗑️  Uninstalling $packageName..." -ForegroundColor Yellow
    try {
        & $pipPath uninstall $packageName -y
        Write-Host "✅ Uninstall command completed" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Could not uninstall $packageName: $_" -ForegroundColor Yellow
    }
    
    # Install the package
    if ($package.Version) {
        $installCmd = "$($package.Name)==$($package.Version)"
    } else {
        $installCmd = "$($package.Name)"
    }
    
    Write-Host "📥 Installing $installCmd..." -ForegroundColor Yellow
    try {
        & $pipPath install $installCmd --force-reinstall --no-cache-dir
        Write-Host "✅ $($package.Name) installed successfully!" -ForegroundColor Green
        
        # Test the import
        Write-Host "🧪 Testing $packageName import..." -ForegroundColor Yellow
        try {
            switch ($packageName) {
                "python-jose" {
                    python -c "import jose; print('✅ jose import successful!')"
                }
                "python-dotenv" {
                    python -c "import dotenv; print('✅ dotenv import successful!')"
                }
                "pydantic-settings" {
                    python -c "import pydantic_settings; print('✅ pydantic_settings import successful!')"
                }
                "google-generativeai" {
                    python -c "import google.generativeai; print('✅ google.generativeai import successful!')"
                }
                "google-auth" {
                    python -c "import google.auth; print('✅ google.auth import successful!')"
                }
                default {
                    python -c "import $packageName; print('✅ $packageName import successful!')"
                }
            }
        } catch {
            Write-Host "❌ $packageName import failed: $_" -ForegroundColor Red
            $failedPackages += "$($package.Name)==$($package.Version): $_"
        }
    } catch {
        Write-Host "❌ Failed to install $($package.Name): $_" -ForegroundColor Red
        $failedPackages += "$($package.Name)==$($package.Version): $_"
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
    Write-Host "`n🎉 All packages fixed successfully!" -ForegroundColor Green
    exit 0
}