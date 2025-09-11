@echo off
title Auto Install Missing Dependencies
color 0A

echo ========================================
echo   AI App Builder - Auto Install Dependencies
echo ========================================
echo.

echo Installing missing dependencies...
echo.

pip install python-multipart python-jose[cryptography] python-dotenv pydantic-settings gitpython

echo.
echo Verifying installation...
echo.

python CHECK_DEPENDENCIES.py

echo.
echo Press any key to close this window...
pause >nul