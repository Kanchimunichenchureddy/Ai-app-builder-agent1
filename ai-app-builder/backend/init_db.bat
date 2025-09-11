@echo off
echo Initializing Database...
echo ======================

REM This script will help you set up the database
echo Please make sure you have MySQL installed and running.
echo.
echo 1. Create a MySQL database named 'ai_app_builder'
echo 2. Create a user 'appuser' with password 'rootpassword'
echo 3. Grant all privileges to 'appuser' on 'ai_app_builder' database
echo.
echo You can run these commands in MySQL:
echo CREATE DATABASE ai_app_builder;
echo CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'rootpassword';
echo GRANT ALL PRIVILEGES ON ai_app_builder.* TO 'appuser'@'localhost';
echo FLUSH PRIVILEGES;
echo.
pause