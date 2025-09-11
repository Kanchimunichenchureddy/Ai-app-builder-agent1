@echo off
REM Batch script to fix package import issues for Python 3.13 compatibility

echo 🔧 Fixing package import issues for Python 3.13 compatibility...

REM Get the current directory
set BACKEND_DIR=%~dp0
echo Working directory: %BACKEND_DIR%

REM Define paths
set VENV_PATH=%BACKEND_DIR%venv

echo Virtual environment path: %VENV_PATH%

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

REM Set environment variable to disable user site-packages
set PYTHONNOUSERSITE=1
echo Disabled user site-packages

REM Packages that need to be fixed
echo.
echo 📦 Fixing packages...

REM FastAPI and related packages with typing.Annotated issues
echo 🧪 Fixing fastapi...
"%PIP_PATH%" uninstall fastapi -y
"%PIP_PATH%" install fastapi==0.104.1 --force-reinstall --no-cache-dir

echo 🧪 Fixing openai...
"%PIP_PATH%" uninstall openai -y
"%PIP_PATH%" install openai==1.3.7 --force-reinstall --no-cache-dir

echo 🧪 Fixing typing_extensions...
"%PIP_PATH%" install typing_extensions --force-reinstall --no-cache-dir

REM Missing packages
echo 🧪 Fixing python-jose[cryptography]...
"%PIP_PATH%" uninstall python-jose -y
"%PIP_PATH%" install python-jose[cryptography]==3.3.0 --force-reinstall --no-cache-dir

echo 🧪 Fixing python-dotenv...
"%PIP_PATH%" uninstall python-dotenv -y
"%PIP_PATH%" install python-dotenv==1.0.0 --force-reinstall --no-cache-dir

echo 🧪 Fixing pydantic-settings...
"%PIP_PATH%" uninstall pydantic-settings -y
"%PIP_PATH%" install pydantic-settings==2.1.0 --force-reinstall --no-cache-dir

echo 🧪 Fixing google-generativeai...
"%PIP_PATH%" uninstall google-generativeai -y
"%PIP_PATH%" install google-generativeai==0.3.2 --force-reinstall --no-cache-dir

echo 🧪 Fixing google-auth...
"%PIP_PATH%" uninstall google-auth -y
"%PIP_PATH%" install google-auth==2.23.4 --force-reinstall --no-cache-dir

REM Updated to more compatible versions for Python 3.13
echo 🧪 Fixing google-auth-oauthlib...
"%PIP_PATH%" uninstall google-auth-oauthlib -y
"%PIP_PATH%" install google-auth-oauthlib==1.2.0 --force-reinstall --no-cache-dir

echo 🧪 Fixing google-auth-httplib2...
"%PIP_PATH%" uninstall google-auth-httplib2 -y
"%PIP_PATH%" install google-auth-httplib2==0.2.0 --force-reinstall --no-cache-dir

echo 🧪 Fixing google-api-python-client...
"%PIP_PATH%" uninstall google-api-python-client -y
"%PIP_PATH%" install google-api-python-client==2.110.0 --force-reinstall --no-cache-dir

echo.
echo 🧪 Testing imports...

REM Test imports
echo Testing jose import...
python -c "import jose; print('✅ jose import successful!')" || echo ❌ jose import failed

echo Testing dotenv import...
python -c "import dotenv; print('✅ dotenv import successful!')" || echo ❌ dotenv import failed

echo Testing pydantic_settings import...
python -c "import pydantic_settings; print('✅ pydantic_settings import successful!')" || echo ❌ pydantic_settings import failed

echo Testing google.generativeai import...
python -c "import google.generativeai; print('✅ google.generativeai import successful!')" || echo ❌ google.generativeai import failed

echo Testing google.auth import...
python -c "import google.auth; print('✅ google.auth import successful!')" || echo ❌ google.auth import failed

echo.
echo 🎉 Package fix process completed!
echo Please check the output above to see if all packages were fixed successfully.
pause