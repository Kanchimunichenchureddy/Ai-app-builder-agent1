@echo off
title Dependency Check
color 0A

echo ========================================
echo   AI App Builder - Dependency Check
echo ========================================
echo.

echo Checking if all required dependencies are installed...
echo.

python CHECK_DEPENDENCIES.py

echo.
echo Press any key to close this window...
pause >nul