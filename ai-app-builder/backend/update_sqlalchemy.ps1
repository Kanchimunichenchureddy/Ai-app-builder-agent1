# PowerShell script to update SQLAlchemy to Python 3.13 compatible version

Write-Host "🔧 Updating SQLAlchemy to Python 3.13 compatible version..." -ForegroundColor Green

# Get the current directory
$backendDir = Get-Location
Write-Host "Working directory: $backendDir" -ForegroundColor Yellow

# Define paths
$venvPath = Join-Path $backendDir "venv"
$requirementsPath = Join-Path $backendDir "requirements.txt"

Write-Host "Virtual environment path: $venvPath" -ForegroundColor Yellow
Write-Host "Requirements file: $requirementsPath" -ForegroundColor Yellow

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

# First, try to uninstall existing SQLAlchemy
Write-Host "🗑️  Uninstalling existing SQLAlchemy..." -ForegroundColor Cyan
try {
    & $pipPath uninstall sqlalchemy -y
    Write-Host "✅ Uninstall command completed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not uninstall SQLAlchemy: $_" -ForegroundColor Yellow
}

# Install the updated SQLAlchemy
Write-Host "📥 Installing SQLAlchemy 2.0.35..." -ForegroundColor Cyan
try {
    & $pipPath install sqlalchemy==2.0.35
    Write-Host "✅ SQLAlchemy 2.0.35 installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install SQLAlchemy: $_" -ForegroundColor Red
    exit 1
}

# Test the import
Write-Host "🧪 Testing SQLAlchemy import..." -ForegroundColor Cyan
try {
    $importTest = python -c "import sqlalchemy; print(f'SQLAlchemy version: {sqlalchemy.__version__}')"
    Write-Host "✅ SQLAlchemy import successful!" -ForegroundColor Green
    Write-Host $importTest -ForegroundColor White
} catch {
    Write-Host "❌ SQLAlchemy import failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host "🎉 SQLAlchemy update completed successfully!" -ForegroundColor Green