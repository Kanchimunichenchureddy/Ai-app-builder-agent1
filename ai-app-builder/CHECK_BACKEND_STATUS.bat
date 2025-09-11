@echo off
title Backend Status Check
color 0A

echo ========================================
echo   AI App Builder - Backend Server Status Check
echo ========================================
echo.

echo Checking if backend server is running...
echo.

python CHECK_BACKEND_STATUS.py

echo.
echo Press any key to close this window...
pause >nul