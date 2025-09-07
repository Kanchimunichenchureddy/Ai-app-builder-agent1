from typing import Dict, Any, List
import os
import json
from pathlib import Path
from .integrations.openai_service import OpenAIService
from .integrations.gemini_service import GeminiService

class CodeGenerator:
    """
    Advanced code generator for creating complete full-stack applications.
    """
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.gemini_service = GeminiService()
        
    async def generate_react_app(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate complete React frontend application."""
        files = {}
        project_type = analysis.get("project_type", "web_app")
        features = analysis.get("features", [])
        
        # Generate main App.js
        files["frontend/src/App.js"] = await self._generate_react_app_js(project_type, features)
        
        # Generate components based on project type
        if project_type == "dashboard":
            files.update(await self._generate_dashboard_components())
        elif project_type == "ecommerce":
            files.update(await self._generate_ecommerce_components())
        elif project_type == "blog":
            files.update(await self._generate_blog_components())
        elif project_type == "chat":
            files.update(await self._generate_chat_components())
        elif project_type == "crm":
            files.update(await self._generate_crm_components())
        else:
            files.update(await self._generate_default_components())
            
        # Generate common components
        files.update(await self._generate_common_components())
        
        # Generate package.json
        files["frontend/package.json"] = self._generate_package_json(project_type, features)
        
        # Generate index.html
        files["frontend/public/index.html"] = self._generate_index_html(project_type)
        
        return files
    
    async def generate_fastapi_app(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate complete FastAPI backend application."""
        files = {}
        project_type = analysis.get("project_type", "web_app")
        features = analysis.get("features", [])
        
        # Generate main.py
        files["backend/app/main.py"] = await self._generate_fastapi_main(project_type, features)
        
        # Generate models
        files.update(await self._generate_fastapi_models(project_type, features))
        
        # Generate API routes
        files.update(await self._generate_fastapi_routes(project_type, features))
        
        # Generate schemas
        files.update(await self._generate_fastapi_schemas(project_type, features))
        
        # Generate services
        files.update(await self._generate_fastapi_services(project_type, features))
        
        # Generate requirements.txt
        files["backend/requirements.txt"] = self._generate_requirements(project_type, features)
        
        return files
    
    async def generate_database_schema(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate MySQL database schema."""
        files = {}
        project_type = analysis.get("project_type", "web_app")
        features = analysis.get("features", [])
        
        # Generate database schema
        schema_sql = await self._generate_mysql_schema(project_type, features)
        files["database/schema.sql"] = schema_sql
        
        # Generate migrations
        migration_sql = await self._generate_mysql_migrations(project_type, features)
        files["database/migrations/001_initial.sql"] = migration_sql
        
        return files
    
    async def generate_deployment_config(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate deployment configurations."""
        files = {}
        project_type = analysis.get("project_type", "web_app")
        
        # Generate Docker files
        files["Dockerfile"] = self._generate_main_dockerfile()
        files["docker-compose.yml"] = self._generate_docker_compose(project_type)
        
        # Generate Vercel config
        files["vercel.json"] = self._generate_vercel_config()
        
        # Generate Netlify config
        files["netlify.toml"] = self._generate_netlify_config()
        
        # Generate GitHub Actions
        files[".github/workflows/deploy.yml"] = self._generate_github_actions()
        
        return files
    
    async def _generate_react_app_js(self, project_type: str, features: List[str]) -> str:
        """Generate main React App.js file."""
        prompt = f"""
        Generate a complete React App.js file for a {project_type} application.
        Features to include: {', '.join(features)}
        
        Requirements:
        - Use React Router for navigation
        - Include authentication if in features
        - Modern React with hooks
        - Responsive design
        - Error boundaries
        - Loading states
        """
        
        return await self.openai_service.generate_code(prompt, "javascript", "react")
    
    async def _generate_dashboard_components(self) -> Dict[str, str]:
        """Generate dashboard-specific React components."""
        components = {}
        
        # Dashboard main component
        components["frontend/src/components/Dashboard/Dashboard.js"] = await self.openai_service.generate_code(
            "Create a responsive dashboard component with grid layout for widgets and charts", 
            "javascript", "react"
        )
        
        # Chart components
        components["frontend/src/components/Charts/LineChart.js"] = await self.openai_service.generate_code(
            "Create a reusable line chart component using Chart.js or similar", 
            "javascript", "react"
        )
        
        components["frontend/src/components/Charts/BarChart.js"] = await self.openai_service.generate_code(
            "Create a reusable bar chart component using Chart.js or similar", 
            "javascript", "react"
        )
        
        # Widget components
        components["frontend/src/components/Widgets/StatCard.js"] = await self.openai_service.generate_code(
            "Create a statistics card widget component with icon and number display", 
            "javascript", "react"
        )
        
        return components
    
    async def _generate_ecommerce_components(self) -> Dict[str, str]:
        """Generate e-commerce specific React components."""
        components = {}
        
        # Product components
        components["frontend/src/components/Products/ProductList.js"] = await self.openai_service.generate_code(
            "Create a product listing component with grid layout, filtering, and pagination", 
            "javascript", "react"
        )
        
        components["frontend/src/components/Products/ProductCard.js"] = await self.openai_service.generate_code(
            "Create a product card component with image, title, price, and add to cart button", 
            "javascript", "react"
        )
        
        # Cart components
        components["frontend/src/components/Cart/Cart.js"] = await self.openai_service.generate_code(
            "Create a shopping cart component with item management and total calculation", 
            "javascript", "react"
        )
        
        components["frontend/src/components/Cart/CartItem.js"] = await self.openai_service.generate_code(
            "Create a cart item component with quantity controls and remove option", 
            "javascript", "react"
        )
        
        # Checkout components
        components["frontend/src/components/Checkout/Checkout.js"] = await self.openai_service.generate_code(
            "Create a checkout component with form validation and Stripe integration", 
            "javascript", "react"
        )
        
        return components
    
    async def _generate_blog_components(self) -> Dict[str, str]:
        """Generate blog-specific React components."""
        components = {}
        
        components["frontend/src/components/Blog/PostList.js"] = await self.openai_service.generate_code(
            "Create a blog post listing component with pagination and search", 
            "javascript", "react"
        )
        
        components["frontend/src/components/Blog/PostCard.js"] = await self.openai_service.generate_code(
            "Create a blog post card component with title, excerpt, date, and read more link", 
            "javascript", "react"
        )
        
        components["frontend/src/components/Blog/PostDetail.js"] = await self.openai_service.generate_code(
            "Create a blog post detail component with content rendering and comments", 
            "javascript", "react"
        )
        
        components["frontend/src/components/Blog/PostEditor.js"] = await self.openai_service.generate_code(
            "Create a rich text editor component for creating and editing blog posts", 
            "javascript", "react"
        )
        
        return components
    
    async def _generate_chat_components(self) -> Dict[str, str]:
        """Generate chat-specific React components."""
        components = {}
        
        components["frontend/src/components/Chat/ChatRoom.js"] = await self.openai_service.generate_code(
            "Create a chat room component with real-time messaging using WebSocket", 
            "javascript", "react"
        )
        
        components["frontend/src/components/Chat/MessageList.js"] = await self.openai_service.generate_code(
            "Create a message list component with auto-scroll and message grouping", 
            "javascript", "react"
        )
        
        components["frontend/src/components/Chat/MessageInput.js"] = await self.openai_service.generate_code(
            "Create a message input component with file upload and emoji support", 
            "javascript", "react"
        )
        
        return components
    
    async def _generate_crm_components(self) -> Dict[str, str]:
        """Generate CRM-specific React components."""
        components = {}
        
        components["frontend/src/components/CRM/ContactList.js"] = await self.openai_service.generate_code(
            "Create a contact list component with search, filter, and pagination", 
            "javascript", "react"
        )
        
        components["frontend/src/components/CRM/ContactCard.js"] = await self.openai_service.generate_code(
            "Create a contact card component with contact information and actions", 
            "javascript", "react"
        )
        
        components["frontend/src/components/CRM/DealPipeline.js"] = await self.openai_service.generate_code(
            "Create a deal pipeline component with drag-and-drop kanban board", 
            "javascript", "react"
        )
        
        return components
    
    async def _generate_default_components(self) -> Dict[str, str]:
        """Generate default components for web applications."""
        components = {}
        
        components["frontend/src/components/Home/Home.js"] = await self.openai_service.generate_code(
            "Create a home page component with hero section and feature highlights", 
            "javascript", "react"
        )
        
        components["frontend/src/components/About/About.js"] = await self.openai_service.generate_code(
            "Create an about page component with company information and team", 
            "javascript", "react"
        )
        
        return components
    
    async def _generate_common_components(self) -> Dict[str, str]:
        """Generate common components used across all project types."""
        components = {}
        
        components["frontend/src/components/Layout/Header.js"] = await self.openai_service.generate_code(
            "Create a responsive header component with navigation and user menu", 
            "javascript", "react"
        )
        
        components["frontend/src/components/Layout/Footer.js"] = await self.openai_service.generate_code(
            "Create a footer component with links and company information", 
            "javascript", "react"
        )
        
        components["frontend/src/components/Layout/Sidebar.js"] = await self.openai_service.generate_code(
            "Create a collapsible sidebar component for navigation", 
            "javascript", "react"
        )
        
        components["frontend/src/components/Auth/Login.js"] = await self.openai_service.generate_code(
            "Create a login component with form validation and error handling", 
            "javascript", "react"
        )
        
        components["frontend/src/components/Auth/Register.js"] = await self.openai_service.generate_code(
            "Create a registration component with form validation", 
            "javascript", "react"
        )
        
        components["frontend/src/components/Common/Loading.js"] = await self.openai_service.generate_code(
            "Create a loading spinner component with different sizes", 
            "javascript", "react"
        )
        
        components["frontend/src/components/Common/Modal.js"] = await self.openai_service.generate_code(
            "Create a reusable modal component with backdrop and close functionality", 
            "javascript", "react"
        )
        
        return components
    
    def _generate_package_json(self, project_type: str, features: List[str]) -> str:
        """Generate package.json for React app."""
        dependencies = {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.8.1",
            "axios": "^1.6.2",
            "styled-components": "^6.1.6"
        }
        
        # Add dependencies based on features
        if "authentication" in features:
            dependencies["react-hook-form"] = "^7.48.2"
            
        if "charts" in features or project_type == "dashboard":
            dependencies["chart.js"] = "^4.4.0"
            dependencies["react-chartjs-2"] = "^5.2.0"
            
        if "payments" in features or project_type == "ecommerce":
            dependencies["@stripe/stripe-js"] = "^2.2.0"
            dependencies["@stripe/react-stripe-js"] = "^2.4.0"
            
        package_json = {
            "name": f"{project_type.replace('_', '-')}-frontend",
            "version": "1.0.0",
            "private": True,
            "dependencies": dependencies,
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            },
            "browserslist": {
                "production": [
                    ">0.2%",
                    "not dead",
                    "not op_mini all"
                ],
                "development": [
                    "last 1 chrome version",
                    "last 1 firefox version",
                    "last 1 safari version"
                ]
            }
        }
        
        return json.dumps(package_json, indent=2)
    
    def _generate_index_html(self, project_type: str) -> str:
        """Generate index.html for React app."""
        app_names = {
            "dashboard": "Analytics Dashboard",
            "ecommerce": "E-commerce Store", 
            "blog": "Blog Platform",
            "chat": "Chat Application",
            "crm": "CRM System",
            "web_app": "Web Application"
        }
        
        app_name = app_names.get(project_type, "Web Application")
        
        return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="{app_name} - Built with AI App Builder" />
    <title>{app_name}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>'''
    
    async def _generate_fastapi_main(self, project_type: str, features: List[str]) -> str:
        """Generate main FastAPI application file."""
        prompt = f"""
        Generate a complete FastAPI main.py file for a {project_type} application.
        Features to include: {', '.join(features)}
        
        Requirements:
        - Include CORS middleware
        - Add authentication middleware if needed
        - Include proper error handling
        - Add health check endpoint
        - Include API documentation
        - Add rate limiting if needed
        """
        
        return await self.openai_service.generate_code(prompt, "python", "fastapi")
    
    async def _generate_fastapi_models(self, project_type: str, features: List[str]) -> Dict[str, str]:
        """Generate SQLAlchemy models."""
        models = {}
        
        # Always include User model
        models["backend/app/models/user.py"] = await self.openai_service.generate_code(
            "Create a SQLAlchemy User model with authentication fields", 
            "python", "sqlalchemy"
        )
        
        # Generate models based on project type
        if project_type == "ecommerce":
            models["backend/app/models/product.py"] = await self.openai_service.generate_code(
                "Create SQLAlchemy models for Product, Category, and Order", 
                "python", "sqlalchemy"
            )
            
        elif project_type == "blog":
            models["backend/app/models/post.py"] = await self.openai_service.generate_code(
                "Create SQLAlchemy models for BlogPost, Category, and Comment", 
                "python", "sqlalchemy"
            )
            
        elif project_type == "chat":
            models["backend/app/models/message.py"] = await self.openai_service.generate_code(
                "Create SQLAlchemy models for ChatRoom, Message, and Participant", 
                "python", "sqlalchemy"
            )
            
        elif project_type == "crm":
            models["backend/app/models/contact.py"] = await self.openai_service.generate_code(
                "Create SQLAlchemy models for Contact, Deal, and Task", 
                "python", "sqlalchemy"
            )
        
        return models
    
    async def _generate_fastapi_routes(self, project_type: str, features: List[str]) -> Dict[str, str]:
        """Generate FastAPI route files."""
        routes = {}
        
        # Always include auth routes
        routes["backend/app/api/auth.py"] = await self.openai_service.generate_code(
            "Create FastAPI authentication routes with JWT token handling", 
            "python", "fastapi"
        )
        
        # Generate routes based on project type
        if project_type == "ecommerce":
            routes["backend/app/api/products.py"] = await self.openai_service.generate_code(
                "Create FastAPI routes for product CRUD operations with pagination", 
                "python", "fastapi"
            )
            routes["backend/app/api/orders.py"] = await self.openai_service.generate_code(
                "Create FastAPI routes for order management and payment processing", 
                "python", "fastapi"
            )
            
        elif project_type == "blog":
            routes["backend/app/api/posts.py"] = await self.openai_service.generate_code(
                "Create FastAPI routes for blog post CRUD operations", 
                "python", "fastapi"
            )
            
        elif project_type == "chat":
            routes["backend/app/api/chat.py"] = await self.openai_service.generate_code(
                "Create FastAPI routes for chat functionality with WebSocket support", 
                "python", "fastapi"
            )
            
        elif project_type == "crm":
            routes["backend/app/api/contacts.py"] = await self.openai_service.generate_code(
                "Create FastAPI routes for contact and deal management", 
                "python", "fastapi"
            )
        
        return routes
    
    async def _generate_fastapi_schemas(self, project_type: str, features: List[str]) -> Dict[str, str]:
        """Generate Pydantic schemas."""
        schemas = {}
        
        schemas["backend/app/schemas/user.py"] = await self.openai_service.generate_code(
            "Create Pydantic schemas for User model with validation", 
            "python", "pydantic"
        )
        
        # Add schemas based on project type
        if project_type == "ecommerce":
            schemas["backend/app/schemas/product.py"] = await self.openai_service.generate_code(
                "Create Pydantic schemas for Product and Order models", 
                "python", "pydantic"
            )
            
        elif project_type == "blog":
            schemas["backend/app/schemas/post.py"] = await self.openai_service.generate_code(
                "Create Pydantic schemas for BlogPost and Comment models", 
                "python", "pydantic"
            )
        
        return schemas
    
    async def _generate_fastapi_services(self, project_type: str, features: List[str]) -> Dict[str, str]:
        """Generate service layer files."""
        services = {}
        
        services["backend/app/services/auth_service.py"] = await self.openai_service.generate_code(
            "Create authentication service with password hashing and JWT tokens", 
            "python", "fastapi"
        )
        
        if "payments" in features:
            services["backend/app/services/payment_service.py"] = await self.openai_service.generate_code(
                "Create payment service with Stripe integration", 
                "python", "fastapi"
            )
        
        return services
    
    def _generate_requirements(self, project_type: str, features: List[str]) -> str:
        """Generate requirements.txt for FastAPI backend."""
        requirements = [
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "sqlalchemy==2.0.23",
            "pymysql==1.1.0",
            "python-multipart==0.0.6",
            "python-jose[cryptography]==3.3.0",
            "passlib[bcrypt]==1.7.4",
            "python-dotenv==1.0.0",
            "pydantic==2.5.0",
            "httpx==0.25.2"
        ]
        
        # Add requirements based on features
        if "payments" in features or project_type == "ecommerce":
            requirements.append("stripe==7.8.0")
            
        if "websockets" in features or project_type == "chat":
            requirements.append("websockets==12.0")
            
        if "email" in features:
            requirements.append("fastapi-mail==1.4.1")
            
        return "\n".join(requirements)
    
    async def _generate_mysql_schema(self, project_type: str, features: List[str]) -> str:
        """Generate MySQL database schema."""
        prompt = f"""
        Generate a complete MySQL database schema for a {project_type} application.
        Features to include: {', '.join(features)}
        
        Requirements:
        - Include proper indexes
        - Add foreign key constraints
        - Include timestamp fields
        - Add user authentication tables
        - Follow best practices for MySQL
        """
        
        return await self.openai_service.generate_code(prompt, "sql", "mysql")
    
    async def _generate_mysql_migrations(self, project_type: str, features: List[str]) -> str:
        """Generate database migration files."""
        prompt = f"""
        Generate initial database migration SQL for a {project_type} application.
        Features to include: {', '.join(features)}
        
        Include:
        - CREATE TABLE statements
        - INSERT default data
        - CREATE INDEX statements
        """
        
        return await self.openai_service.generate_code(prompt, "sql", "mysql")
    
    def _generate_main_dockerfile(self) -> str:
        """Generate main Dockerfile for the application."""
        return '''FROM node:18-alpine as frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim as backend
WORKDIR /app
RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev pkg-config
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./
COPY --from=frontend-build /app/frontend/build ./static

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]'''
    
    def _generate_docker_compose(self, project_type: str) -> str:
        """Generate docker-compose.yml file."""
        return '''version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: app_db
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"
      
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://root:password@mysql:3306/app_db
    depends_on:
      - mysql
      
volumes:
  mysql_data:'''
    
    def _generate_vercel_config(self) -> str:
        """Generate Vercel deployment configuration."""
        return json.dumps({
            "builds": [
                {"src": "frontend/build/**", "use": "@vercel/static"},
                {"src": "backend/app/main.py", "use": "@vercel/python"}
            ],
            "routes": [
                {"src": "/api/(.*)", "dest": "backend/app/main.py"},
                {"src": "/(.*)", "dest": "frontend/build/$1"}
            ]
        }, indent=2)
    
    def _generate_netlify_config(self) -> str:
        """Generate Netlify deployment configuration."""
        return '''[build]
  command = "cd frontend && npm run build"
  publish = "frontend/build"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200'''
    
    def _generate_github_actions(self) -> str:
        """Generate GitHub Actions workflow."""
        return '''name: Deploy Application

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install frontend dependencies
      run: |
        cd frontend
        npm ci
        
    - name: Build frontend
      run: |
        cd frontend
        npm run build
        
    - name: Install backend dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        
    - name: Deploy to production
      run: |
        echo "Deploy your application here"'''