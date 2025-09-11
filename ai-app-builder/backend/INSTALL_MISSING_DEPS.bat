@echo off
title Install Missing Dependencies
color 0A

echo ========================================
echo   AI App Builder - Missing Dependency Installer
echo ========================================
echo.

echo Installing missing dependencies...
echo.

python INSTALL_MISSING_DEPS.py

echo.
echo Press any key to close this window...
pause >nul