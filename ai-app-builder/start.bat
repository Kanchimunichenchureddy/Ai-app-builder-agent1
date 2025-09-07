@echo off
REM AI App Builder - Quick Start Script for Windows
REM This script sets up and runs the AI App Builder Agent

echo 🚀 AI App Builder Agent - Quick Start
echo ======================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed

REM Create environment files if they don't exist
if not exist backend\.env (
    echo 📝 Creating backend environment file...
    copy backend\.env.example backend\.env
    echo ℹ️  Please edit backend\.env with your API keys
)

if not exist frontend\.env (
    echo 📝 Creating frontend environment file...
    copy frontend\.env.example frontend\.env
)

REM Handle command line arguments
if "%1"=="dev" (
    goto start_dev
) else if "%1"=="prod" (
    goto start_prod
) else if "%1"=="stop" (
    goto stop_services
) else if "%1"=="logs" (
    goto show_logs
) else if "%1"=="status" (
    goto show_status
) else if "%1"=="restart" (
    goto restart_services
) else (
    goto show_usage
)

:start_dev
echo 🔧 Starting development environment...
docker-compose -f deployment\docker-compose.dev.yml up --build
goto end

:start_prod
echo 🚀 Starting production environment...
docker-compose -f deployment\docker-compose.yml up -d --build

echo ✅ AI App Builder is starting up!
echo 📝 Services:
echo    🌐 Frontend: http://localhost:3000
echo    🔧 Backend API: http://localhost:8000
echo    📚 API Docs: http://localhost:8000/docs
echo    🗄️  Database: localhost:3306

echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo 🎉 AI App Builder is ready!
echo 👤 Demo Login:
echo    📧 Email: demo@appforge.dev
echo    🔑 Password: demo123

echo 🌐 Opening browser...
start http://localhost:3000
goto end

:stop_services
echo 🛑 Stopping services...
docker-compose -f deployment\docker-compose.yml down
docker-compose -f deployment\docker-compose.dev.yml down
echo ✅ Services stopped
goto end

:show_logs
echo 📋 Showing logs...
docker-compose -f deployment\docker-compose.yml logs -f
goto end

:show_status
echo 📊 Service Status:
docker-compose -f deployment\docker-compose.yml ps
goto end

:restart_services
call :stop_services
timeout /t 2 /nobreak >nul
call :start_prod
goto end

:show_usage
echo Usage:
echo   %0 dev     - Start development environment (with hot reload)
echo   %0 prod    - Start production environment
echo   %0 stop    - Stop all services
echo   %0 restart - Restart production environment
echo   %0 logs    - Show service logs
echo   %0 status  - Show service status
echo.
echo Quick Start:
echo   %0 prod    # Start the AI App Builder
echo.
echo 🎯 What this AI Agent can build:
echo    📊 Dashboard applications
echo    🛒 E-commerce platforms
echo    📝 Blog/CMS systems
echo    💬 Chat applications
echo    👥 CRM systems
echo    🔧 Custom web applications
echo.
echo 🔗 After starting, visit: http://localhost:3000

:end
pause