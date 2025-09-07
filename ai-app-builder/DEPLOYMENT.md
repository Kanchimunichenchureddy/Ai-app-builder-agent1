# 🚀 AI App Builder Agent - Deployment Guide

## 🎯 **Quick Start (Recommended)**

### **Option 1: Windows**
```bash
# Run this command in the ai-app-builder directory
start.bat prod
```

### **Option 2: Linux/Mac**
```bash
# Make the script executable and run
chmod +x start.sh
./start.sh prod
```

### **Option 3: Manual Docker Setup**
```bash
# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start the application
docker-compose -f deployment/docker-compose.yml up -d --build
```

---

## 🔧 **Configuration**

### **1. Backend Configuration (`backend/.env`)**
```env
# Database
DB_HOST=mysql
DB_PORT=3306
DB_USER=appuser
DB_PASSWORD=your_secure_password
DB_NAME=ai_app_builder

# Security
SECRET_KEY=your-super-secret-key-min-32-characters-long
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Services (Optional - for enhanced features)
OPENAI_API_KEY=sk-your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# External APIs (Optional)
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
```

### **2. Frontend Configuration (`frontend/.env`)**
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_APP_NAME="AI App Builder Agent"
```

---

## 🌐 **Access Your AI Agent**

After deployment, access these URLs:

| Service | URL | Description |
|---------|-----|-------------|
| **🏠 Main App** | http://localhost:3000 | AI App Builder Interface |
| **🔧 Backend API** | http://localhost:8000 | FastAPI Backend |
| **📚 API Docs** | http://localhost:8000/docs | Interactive API Documentation |
| **🗄️ Database** | localhost:3306 | MySQL Database |

### **Demo Login Credentials**
- **📧 Email:** `demo@appforge.dev`
- **🔑 Password:** `demo123`

---

## 🎯 **How to Use Your AI Agent**

### **1. Login**
- Open http://localhost:3000
- Use demo credentials or register a new account

### **2. Build Unlimited Applications**
Simply tell the AI what you want:

**💬 Example Prompts:**
- *"Build me a task management app with real-time collaboration"*
- *"Create an e-commerce store with Stripe payments"*
- *"Build a social media dashboard with analytics"*
- *"Create a blog platform with comments and admin panel"*
- *"Build a CRM system with contact management"*

### **3. Project Types Supported**
- **📊 Dashboard** - Analytics dashboards with charts
- **🛒 E-commerce** - Online stores with payments
- **📝 Blog/CMS** - Content management systems
- **💬 Chat Apps** - Real-time messaging platforms
- **👥 CRM** - Customer relationship management
- **🔧 Custom Web Apps** - Any web application you can imagine

### **4. Deployment Options**
- **🐳 Docker** - Local containers
- **⚡ Vercel** - Frontend hosting
- **🌐 Netlify** - JAMstack deployment
- **☁️ AWS/GCP/Azure** - Cloud platforms (coming soon)

---

## 🛠️ **Development Mode**

For development with hot reload:

```bash
# Windows
start.bat dev

# Linux/Mac
./start.sh dev
```

---

## 🔧 **Manual Commands**

### **Start Services**
```bash
docker-compose -f deployment/docker-compose.yml up -d
```

### **Stop Services**
```bash
docker-compose -f deployment/docker-compose.yml down
```

### **View Logs**
```bash
docker-compose -f deployment/docker-compose.yml logs -f
```

### **Rebuild and Restart**
```bash
docker-compose -f deployment/docker-compose.yml down
docker-compose -f deployment/docker-compose.yml up -d --build
```

---

## 📋 **Requirements**

### **System Requirements**
- **Docker** (with Docker Compose)
- **4GB RAM minimum** (8GB recommended)
- **5GB free disk space**
- **Windows 10/11, macOS, or Linux**

### **Optional (for enhanced features)**
- **OpenAI API Key** - For advanced AI code generation
- **Gemini API Key** - Alternative AI provider
- **Stripe Account** - For payment integrations in generated apps
- **Vercel/Netlify CLI** - For deployment to cloud platforms

---

## 🆘 **Troubleshooting**

### **Common Issues**

**1. Port Already in Use**
```bash
# Stop any conflicting services
docker-compose down
# Or change ports in docker-compose.yml
```

**2. Database Connection Failed**
```bash
# Wait for MySQL to fully start
docker-compose logs mysql
# Check if MySQL container is healthy
docker-compose ps
```

**3. Permission Errors (Linux/Mac)**
```bash
# Fix file permissions
sudo chown -R $USER:$USER ./ai-app-builder
chmod +x start.sh
```

**4. Docker Issues**
```bash
# Restart Docker service
sudo systemctl restart docker  # Linux
# Or restart Docker Desktop (Windows/Mac)

# Clean Docker cache
docker system prune -a
```

---

## 🔒 **Security Notes**

### **Production Deployment**
1. **Change default passwords** in `.env` files
2. **Use strong SECRET_KEY** (32+ characters)
3. **Enable HTTPS** with reverse proxy
4. **Restrict database access** to localhost
5. **Use environment-specific configurations**

### **API Keys**
- Store API keys securely in environment variables
- Never commit API keys to version control
- Use different keys for development and production

---

## 🚀 **Production Deployment**

### **Docker Production Setup**
```bash
# Use production docker-compose
docker-compose -f deployment/docker-compose.yml up -d --build

# With Nginx reverse proxy
docker-compose -f deployment/docker-compose.yml up -d nginx
```

### **Cloud Deployment**
- Configure your cloud provider
- Update environment variables for production
- Set up proper domain and SSL certificates
- Configure CI/CD pipeline with provided GitHub Actions

---

## 🎉 **Success!**

Your AI App Builder Agent is now running! 

**🌟 What You Can Do:**
- Build unlimited full-stack applications
- Generate React frontends automatically  
- Create FastAPI backends with MySQL
- Deploy to multiple platforms
- Modify existing projects with natural language
- Use pre-built templates for rapid development

**🔗 Quick Links:**
- **Main App:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **GitHub:** Your repository URL
- **Support:** Check the troubleshooting section above

**Happy Building! 🚀**