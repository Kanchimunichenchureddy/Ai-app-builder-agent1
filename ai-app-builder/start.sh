#!/bin/bash

# AI App Builder - Quick Start Script
# This script sets up and runs the AI App Builder Agent

set -e

echo "🚀 AI App Builder Agent - Quick Start"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose are installed${NC}"

# Create environment files if they don't exist
if [ ! -f backend/.env ]; then
    echo -e "${YELLOW}📝 Creating backend environment file...${NC}"
    cp backend/.env.example backend/.env
    echo -e "${BLUE}ℹ️  Please edit backend/.env with your API keys${NC}"
fi

if [ ! -f frontend/.env ]; then
    echo -e "${YELLOW}📝 Creating frontend environment file...${NC}"
    cp frontend/.env.example frontend/.env
fi

# Function to start development environment
start_dev() {
    echo -e "${BLUE}🔧 Starting development environment...${NC}"
    docker-compose -f deployment/docker-compose.dev.yml up --build
}

# Function to start production environment
start_prod() {
    echo -e "${BLUE}🚀 Starting production environment...${NC}"
    docker-compose -f deployment/docker-compose.yml up -d --build
    
    echo -e "${GREEN}✅ AI App Builder is starting up!${NC}"
    echo -e "${BLUE}📝 Services:${NC}"
    echo -e "   🌐 Frontend: http://localhost:3000"
    echo -e "   🔧 Backend API: http://localhost:8000"
    echo -e "   📚 API Docs: http://localhost:8000/docs"
    echo -e "   🗄️  Database: localhost:3306"
    
    echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
    sleep 10
    
    echo -e "${GREEN}🎉 AI App Builder is ready!${NC}"
    echo -e "${BLUE}👤 Demo Login:${NC}"
    echo -e "   📧 Email: demo@appforge.dev"
    echo -e "   🔑 Password: demo123"
}

# Function to stop services
stop_services() {
    echo -e "${YELLOW}🛑 Stopping services...${NC}"
    docker-compose -f deployment/docker-compose.yml down
    docker-compose -f deployment/docker-compose.dev.yml down
    echo -e "${GREEN}✅ Services stopped${NC}"
}

# Function to show logs
show_logs() {
    echo -e "${BLUE}📋 Showing logs...${NC}"
    docker-compose -f deployment/docker-compose.yml logs -f
}

# Function to show status
show_status() {
    echo -e "${BLUE}📊 Service Status:${NC}"
    docker-compose -f deployment/docker-compose.yml ps
}

# Main menu
case "${1:-}" in
    "dev")
        start_dev
        ;;
    "prod")
        start_prod
        ;;
    "stop")
        stop_services
        ;;
    "logs")
        show_logs
        ;;
    "status")
        show_status
        ;;
    "restart")
        stop_services
        sleep 2
        start_prod
        ;;
    *)
        echo -e "${BLUE}Usage:${NC}"
        echo -e "  $0 dev     - Start development environment (with hot reload)"
        echo -e "  $0 prod    - Start production environment"
        echo -e "  $0 stop    - Stop all services"
        echo -e "  $0 restart - Restart production environment"
        echo -e "  $0 logs    - Show service logs"
        echo -e "  $0 status  - Show service status"
        echo ""
        echo -e "${YELLOW}Quick Start:${NC}"
        echo -e "  $0 prod    # Start the AI App Builder"
        echo ""
        echo -e "${GREEN}🎯 What this AI Agent can build:${NC}"
        echo -e "   📊 Dashboard applications"
        echo -e "   🛒 E-commerce platforms"
        echo -e "   📝 Blog/CMS systems"
        echo -e "   💬 Chat applications"
        echo -e "   👥 CRM systems"
        echo -e "   🔧 Custom web applications"
        echo ""
        echo -e "${BLUE}🔗 After starting, visit: http://localhost:3000${NC}"
        ;;
esac