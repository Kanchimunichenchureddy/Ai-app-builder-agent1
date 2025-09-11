@echo off
title Detailed Dependency Check
color 0A

echo ========================================
echo   AI App Builder - Detailed Dependency Check
echo ========================================
echo.

echo Checking required packages with detailed information...
echo.

python CHECK_DEPENDENCIES_DETAILED.py

echo.
echo Press any key to close this window...
pause >nul