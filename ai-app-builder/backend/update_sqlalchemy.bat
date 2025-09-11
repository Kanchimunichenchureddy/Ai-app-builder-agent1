@echo off
REM Batch script to update SQLAlchemy to Python 3.13 compatible version

echo 🔧 Updating SQLAlchemy to Python 3.13 compatible version...

REM Get the current directory
set BACKEND_DIR=%~dp0
echo Working directory: %BACKEND_DIR%

REM Define paths
set VENV_PATH=%BACKEND_DIR%venv
set REQUIREMENTS_PATH=%BACKEND_DIR%requirements.txt

echo Virtual environment path: %VENV_PATH%
echo Requirements file: %REQUIREMENTS_PATH%

REM Check if virtual environment exists
if exist "%VENV_PATH%" (
    echo ✅ Virtual environment found
    set PIP_PATH=%VENV_PATH%\Scripts\pip.exe
) else (
    echo ⚠️  Virtual environment not found, using system pip
    set PIP_PATH=pip
)

REM Check if pip exists
if exist "%PIP_PATH%" (
    echo ✅ Pip found at: %PIP_PATH%
) else (
    echo ⚠️  Pip not found at expected path, using 'pip' command
    set PIP_PATH=pip
)

REM First, try to uninstall existing SQLAlchemy
echo 🗑️  Uninstalling existing SQLAlchemy...
"%PIP_PATH%" uninstall sqlalchemy -y
if %errorlevel% neq 0 (
    echo ⚠️  Could not uninstall SQLAlchemy
) else (
    echo ✅ Uninstall command completed
)

REM Install the updated SQLAlchemy
echo 📥 Installing SQLAlchemy 2.0.35...
"%PIP_PATH%" install sqlalchemy==2.0.35
if %errorlevel% neq 0 (
    echo ❌ Failed to install SQLAlchemy
    exit /b 1
) else (
    echo ✅ SQLAlchemy 2.0.35 installed successfully!
)

REM Test the import
echo 🧪 Testing SQLAlchemy import...
python -c "import sqlalchemy; print(f'SQLAlchemy version: {sqlalchemy.__version__}')"
if %errorlevel% neq 0 (
    echo ❌ SQLAlchemy import failed
    exit /b 1
) else (
    echo ✅ SQLAlchemy import successful!
)

echo 🎉 SQLAlchemy update completed successfully!
pause