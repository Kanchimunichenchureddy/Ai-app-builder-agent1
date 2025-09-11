# PowerShell script to downgrade SQLAlchemy to a version compatible with Python 3.13

Write-Host "🔧 Emergency SQLAlchemy downgrade for Python 3.13 compatibility..." -ForegroundColor Green

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

# Try to uninstall current SQLAlchemy
Write-Host "`n🗑️  Uninstalling current SQLAlchemy..." -ForegroundColor Yellow
try {
    & $pipPath uninstall sqlalchemy -y
    Write-Host "✅ Uninstall command completed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not uninstall SQLAlchemy: $_" -ForegroundColor Yellow
}

# Try multiple versions of SQLAlchemy that might work with Python 3.13
$sqlalchemyVersions = @(
    "2.0.35",  # Our updated version
    "2.0.30",  # Slightly older version
    "2.0.25",  # Even older version
    "1.4.46",  # Last 1.4.x version
    "1.4.41"   # Known stable version
)

foreach ($version in $sqlalchemyVersions) {
    Write-Host "`n📥 Trying SQLAlchemy $version..." -ForegroundColor Yellow
    try {
        & $pipPath install "sqlalchemy==$version" --force-reinstall --no-cache-dir
        Write-Host "✅ SQLAlchemy $version installed successfully!" -ForegroundColor Green
        
        # Test the import
        Write-Host "🧪 Testing SQLAlchemy $version import..." -ForegroundColor Yellow
        try {
            python -c "import sqlalchemy; print(f'SUCCESS: SQLAlchemy version {sqlalchemy.__version__}')"
            Write-Host "✅ SQLAlchemy $version import test succeeded!" -ForegroundColor Green
            Write-Host "`n🎉 SQLAlchemy downgrade completed successfully!" -ForegroundColor Green
            exit 0
        } catch {
            Write-Host "❌ SQLAlchemy $version import test failed: $_" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Failed to install SQLAlchemy $version: $_" -ForegroundColor Red
    }
}

Write-Host "`n💥 All SQLAlchemy versions failed to install properly." -ForegroundColor Red
Write-Host "`n💡 Manual fix options:" -ForegroundColor Yellow
Write-Host "1. Try installing a specific older version:" -ForegroundColor Yellow
Write-Host "   pip install sqlalchemy==1.4.41 --force-reinstall --no-cache-dir" -ForegroundColor White
Write-Host "2. Check if there are conflicting packages:" -ForegroundColor Yellow
Write-Host "   pip list | findstr sqlalchemy" -ForegroundColor White
exit 1