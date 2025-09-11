@echo off
title Backend Verification
color 0A

echo ========================================
echo   AI App Builder - Backend Verification
echo ========================================
echo.

echo Checking if backend service is running...
echo.

python VERIFY_BACKEND.py

echo.
echo Press any key to close this window...
pause >nul