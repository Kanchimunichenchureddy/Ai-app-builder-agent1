@echo off
title Install All Dependencies
color 0A

echo ========================================
echo   AI App Builder - Install All Dependencies
echo ========================================
echo.

echo Installing all dependencies from requirements.txt...
echo.

pip install -r requirements.txt

echo.
echo Verifying installation...
echo.

python CHECK_DEPENDENCIES.py

echo.
echo Press any key to close this window...
pause >nul