// Template Service for AI App Builder
// Generates complete application templates with React + FastAPI + MySQL

class TemplateService {
  constructor() {
    this.templates = {
      dashboard: this.getDashboardTemplate(),
      ecommerce: this.getEcommerceTemplate(),
      blog: this.getBlogTemplate(),
      chat: this.getChatTemplate(),
      crm: this.getCrmTemplate(),
      saas: this.getSaasTemplate()
    };
    
    // Supported technology stacks
    this.techStacks = {
      frontend: {
        react: { name: 'React.js', description: 'Modern React with hooks', icon: '⚛️' },
        nextjs: { name: 'Next.js', description: 'Full-stack React with SSR', icon: '🔺' },
        vue: { name: 'Vue.js', description: 'Progressive JavaScript framework', icon: '💚' },
        angular: { name: 'Angular', description: 'Enterprise TypeScript framework', icon: '🅰️' },
        react_native: { name: 'React Native', description: 'Cross-platform mobile', icon: '📱' },
        flutter: { name: 'Flutter', description: 'Cross-platform with Dart', icon: '🐦' }
      },
      backend: {
        fastapi: { name: 'FastAPI', description: 'High-performance Python API', icon: '🚀' },
        express: { name: 'Express.js', description: 'Fast Node.js framework', icon: '🟢' },
        nestjs: { name: 'NestJS', description: 'Progressive Node.js', icon: '🦅' },
        django: { name: 'Django', description: 'Python web framework', icon: '🐍' },
        spring_boot: { name: 'Spring Boot', description: 'Enterprise Java', icon: '☕' },
        gin: { name: 'Gin', description: 'Lightweight Go framework', icon: '🐹' }
      },
      database: {
        mysql: { name: 'MySQL', description: 'Relational database', icon: '🐬' },
        postgresql: { name: 'PostgreSQL', description: 'Advanced relational DB', icon: '🐘' },
        mongodb: { name: 'MongoDB', description: 'Document database', icon: '🍃' },
        redis: { name: 'Redis', description: 'In-memory data store', icon: '🔴' },
        sqlite: { name: 'SQLite', description: 'Embedded database', icon: '📄' },
        firebase: { name: 'Firebase', description: 'Google cloud database', icon: '🔥' }
      }
    };
  }

  // Generate complete project structure based on template and tech stack
  async generateProject(templateId, projectName, customFeatures = [], techStack = null) {
    const template = this.templates[templateId];
    if (!template) {
      throw new Error(`Template ${templateId} not found`);
    }

    // Use provided tech stack or default
    const selectedTechStack = techStack || {
      frontend: 'react',
      backend: 'fastapi',
      database: 'mysql'
    };

    const project = {
      name: projectName,
      type: templateId,
      description: template.description,
      features: [...template.features, ...customFeatures],
      techStack: selectedTechStack,
      structure: this.generateProjectStructure(template, selectedTechStack),
      files: await this.generateAllFiles(template, projectName, selectedTechStack),
      database: this.generateDatabaseSchema(template, selectedTechStack.database),
      deployment: this.generateDeploymentConfig(template, projectName, selectedTechStack)
    };

    return project;
  }

  // Dashboard Template
  getDashboardTemplate() {
    return {
      id: 'dashboard',
      name: 'Analytics Dashboard',
      description: 'Business intelligence dashboard with charts, KPIs, and real-time data',
      features: [
        'user_authentication',
        'data_visualization',
        'real_time_updates',
        'export_reports',
        'role_based_access',
        'responsive_design'
      ],
      techStack: {
        frontend: 'react',
        backend: 'fastapi',
        database: 'mysql',
        charts: 'chart.js'
      },
      components: {
        frontend: [
          'Dashboard.js',
          'Charts/LineChart.js',
          'Charts/BarChart.js', 
          'Charts/PieChart.js',
          'Widgets/KPICard.js',
          'Widgets/StatCard.js',
          'Reports/ReportGenerator.js',
          'Layout/DashboardLayout.js'
        ],
        backend: [
          'analytics_router.py',
          'data_processor.py',
          'report_generator.py',
          'websocket_manager.py'
        ]
      },
      database: {
        tables: ['users', 'dashboard_data', 'reports', 'user_preferences']
      }
    };
  }

  // E-commerce Template
  getEcommerceTemplate() {
    return {
      id: 'ecommerce',
      name: 'E-commerce Store',
      description: 'Complete online store with products, cart, and payments',
      features: [
        'user_authentication',
        'product_catalog',
        'shopping_cart',
        'payment_processing',
        'order_management',
        'inventory_tracking',
        'admin_panel',
        'search_functionality'
      ],
      techStack: {
        frontend: 'react',
        backend: 'fastapi',
        database: 'mysql',
        payments: 'stripe'
      },
      components: {
        frontend: [
          'Products/ProductList.js',
          'Products/ProductDetail.js',
          'Cart/ShoppingCart.js',
          'Checkout/CheckoutForm.js',
          'Orders/OrderHistory.js',
          'Admin/ProductManager.js',
          'Search/SearchResults.js'
        ],
        backend: [
          'products_router.py',
          'cart_router.py',
          'orders_router.py',
          'payments_router.py',
          'inventory_manager.py'
        ]
      },
      database: {
        tables: ['users', 'products', 'categories', 'orders', 'order_items', 'cart_items', 'inventory']
      }
    };
  }

  // Blog Template  
  getBlogTemplate() {
    return {
      id: 'blog',
      name: 'Blog & CMS',
      description: 'Content management system with rich editor and SEO',
      features: [
        'user_authentication',
        'rich_text_editor',
        'comment_system',
        'category_management',
        'seo_optimization',
        'media_management',
        'social_sharing'
      ],
      techStack: {
        frontend: 'react',
        backend: 'fastapi',
        database: 'mysql',
        editor: 'quill'
      },
      components: {
        frontend: [
          'Blog/PostList.js',
          'Blog/PostDetail.js',
          'Editor/RichTextEditor.js',
          'Comments/CommentSection.js',
          'Categories/CategoryFilter.js',
          'Admin/PostManager.js'
        ],
        backend: [
          'posts_router.py',
          'comments_router.py',
          'categories_router.py',
          'media_router.py',
          'seo_manager.py'
        ]
      },
      database: {
        tables: ['users', 'posts', 'categories', 'comments', 'media', 'tags', 'post_tags']
      }
    };
  }

  // Chat Template
  getChatTemplate() {
    return {
      id: 'chat',
      name: 'Chat Application',
      description: 'Real-time messaging with rooms and file sharing',
      features: [
        'user_authentication',
        'real_time_messaging',
        'chat_rooms',
        'file_sharing',
        'emoji_support',
        'push_notifications',
        'message_history'
      ],
      techStack: {
        frontend: 'react',
        backend: 'fastapi',
        database: 'mysql',
        realtime: 'websockets'
      },
      components: {
        frontend: [
          'Chat/ChatRoom.js',
          'Chat/MessageList.js',
          'Chat/MessageInput.js',
          'Chat/RoomList.js',
          'FileUpload/FileUploader.js',
          'Notifications/NotificationCenter.js'
        ],
        backend: [
          'chat_router.py',
          'websocket_manager.py',
          'file_manager.py',
          'notification_service.py'
        ]
      },
      database: {
        tables: ['users', 'chat_rooms', 'messages', 'participants', 'files', 'notifications']
      }
    };
  }

  // CRM Template
  getCrmTemplate() {
    return {
      id: 'crm',
      name: 'CRM System',
      description: 'Customer relationship management with sales pipeline',
      features: [
        'user_authentication',
        'contact_management',
        'deal_pipeline',
        'task_tracking',
        'sales_reports',
        'email_integration',
        'calendar_integration'
      ],
      techStack: {
        frontend: 'react',
        backend: 'fastapi',
        database: 'mysql',
        calendar: 'fullcalendar'
      },
      components: {
        frontend: [
          'Contacts/ContactList.js',
          'Contacts/ContactDetail.js',
          'Deals/DealPipeline.js',
          'Tasks/TaskManager.js',
          'Reports/SalesReports.js',
          'Calendar/CalendarView.js'
        ],
        backend: [
          'contacts_router.py',
          'deals_router.py',
          'tasks_router.py',
          'reports_router.py',
          'email_service.py'
        ]
      },
      database: {
        tables: ['users', 'contacts', 'companies', 'deals', 'tasks', 'activities', 'notes']
      }
    };
  }

  // SaaS Template
  getSaasTemplate() {
    return {
      id: 'saas',
      name: 'SaaS Platform',
      description: 'Multi-tenant SaaS with subscriptions and billing',
      features: [
        'user_authentication',
        'multi_tenancy',
        'subscription_billing',
        'api_management',
        'usage_analytics',
        'team_management',
        'role_permissions'
      ],
      techStack: {
        frontend: 'react',
        backend: 'fastapi',
        database: 'mysql',
        billing: 'stripe'
      },
      components: {
        frontend: [
          'Tenants/TenantDashboard.js',
          'Billing/SubscriptionManager.js',
          'Users/TeamManager.js',
          'API/ApiKeyManager.js',
          'Analytics/UsageChart.js',
          'Settings/PlanSettings.js'
        ],
        backend: [
          'tenants_router.py',
          'billing_router.py',
          'api_keys_router.py',
          'usage_tracker.py',
          'subscription_manager.py'
        ]
      },
      database: {
        tables: ['tenants', 'users', 'subscriptions', 'api_keys', 'usage_logs', 'plans']
      }
    };
  }

  // Generate project folder structure
  generateProjectStructure(template) {
    return {
      frontend: {
        src: {
          components: this.createComponentStructure(template.components.frontend),
          pages: {
            'Home.js': null,
            'Login.js': null,
            'Dashboard.js': null
          },
          services: {
            'api.js': null,
            'auth.js': null
          },
          styles: {
            'globals.css': null,
            'components.css': null
          },
          utils: {
            'helpers.js': null,
            'constants.js': null
          }
        },
        public: {
          'index.html': null,
          'favicon.ico': null
        }
      },
      backend: {
        app: {
          api: this.createBackendStructure(template.components.backend),
          models: this.createModelStructure(template.database.tables),
          schemas: {},
          services: {},
          core: {
            'config.py': null,
            'database.py': null,
            'security.py': null
          }
        }
      },
      database: {
        migrations: {},
        seeds: {}
      },
      deployment: {
        'docker-compose.yml': null,
        'Dockerfile.frontend': null,
        'Dockerfile.backend': null
      }
    };
  }

  createComponentStructure(components) {
    const structure = {};
    components.forEach(component => {
      if (component.includes('/')) {
        const [folder, file] = component.split('/');
        if (!structure[folder]) structure[folder] = {};
        structure[folder][file] = null;
      } else {
        structure[component] = null;
      }
    });
    return structure;
  }

  createBackendStructure(routers) {
    const structure = {};
    routers.forEach(router => {
      structure[router] = null;
    });
    return structure;
  }

  createModelStructure(tables) {
    const structure = {};
    tables.forEach(table => {
      structure[`${table}.py`] = null;
    });
    return structure;
  }

  // Generate all project files with actual code
  async generateAllFiles(template, projectName) {
    const files = {};
    
    // Generate package.json
    files['frontend/package.json'] = this.generatePackageJson(template, projectName);
    
    // Generate main App.js
    files['frontend/src/App.js'] = this.generateAppJs(template);
    
    // Generate FastAPI main.py
    files['backend/app/main.py'] = this.generateMainPy(template);
    
    // Generate database models
    template.database.tables.forEach(table => {
      files[`backend/app/models/${table}.py`] = this.generateModel(table, template);
    });
    
    // Generate API routers
    template.components.backend.forEach(router => {
      files[`backend/app/api/${router}`] = this.generateRouter(router, template);
    });
    
    // Generate React components
    template.components.frontend.forEach(component => {
      files[`frontend/src/components/${component}`] = this.generateComponent(component, template);
    });
    
    // Generate requirements.txt
    files['backend/requirements.txt'] = this.generateRequirements(template);
    
    return files;
  }

  generatePackageJson(template, projectName) {
    const dependencies = {
      "react": "^18.2.0",
      "react-dom": "^18.2.0",
      "react-router-dom": "^6.8.1",
      "axios": "^1.6.2",
      "styled-components": "^6.1.6"
    };

    if (template.techStack.charts === 'chart.js') {
      dependencies["chart.js"] = "^4.4.0";
      dependencies["react-chartjs-2"] = "^5.2.0";
    }

    if (template.techStack.editor === 'quill') {
      dependencies["react-quill"] = "^2.0.0";
    }

    if (template.features.includes('payment_processing')) {
      dependencies["@stripe/stripe-js"] = "^2.2.0";
      dependencies["@stripe/react-stripe-js"] = "^2.4.0";
    }

    return JSON.stringify({
      "name": `${projectName.toLowerCase().replace(/\s+/g, '-')}-frontend`,
      "version": "1.0.0",
      "private": true,
      "dependencies": dependencies,
      "scripts": {
        "start": "react-scripts start",
        "build": "react-scripts build",
        "test": "react-scripts test",
        "eject": "react-scripts eject"
      }
    }, null, 2);
  }

  generateAppJs(template) {
    return `import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled, { createGlobalStyle } from 'styled-components';

// Components
import Navbar from './components/Layout/Navbar';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';

// Global Styles
const GlobalStyle = createGlobalStyle\`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #f8fafc;
    color: #1a202c;
  }
\`;

const AppContainer = styled.div\`
  min-height: 100vh;
\`;

function App() {
  return (
    <Router>
      <GlobalStyle />
      <AppContainer>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </AppContainer>
    </Router>
  );
}

export default App;`;
  }

  generateMainPy(template) {
    const imports = [
      'from fastapi import FastAPI, Depends',
      'from fastapi.middleware.cors import CORSMiddleware',
      'from sqlalchemy.orm import Session'
    ];

    if (template.features.includes('real_time_messaging')) {
      imports.push('from fastapi import WebSocket');
    }

    return `${imports.join('\n')}

from .core.config import settings
from .core.database import get_db, create_tables
${template.components.backend.map(router => 
  `from .api import ${router.replace('.py', '').replace('_router', '')}`
).join('\n')}

app = FastAPI(
    title="${template.name} API",
    version="1.0.0",
    description="Generated by AI App Builder"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
${template.components.backend.map(router => {
  const routerName = router.replace('.py', '').replace('_router', '');
  return `app.include_router(${routerName}.router, prefix="/api/${routerName}", tags=["${routerName.title()}"])`;
}).join('\n')}

@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/")
async def root():
    return {"message": "${template.name} API", "status": "running"}`;
  }

  generateModel(tableName, template) {
    return `from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class ${this.capitalize(tableName.slice(0, -1))}(Base):
    __tablename__ = "${tableName}"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Add specific fields based on table type
    ${this.generateModelFields(tableName)}`;
  }

  generateModelFields(tableName) {
    const fields = {
      'users': `
    email = Column(String(255), unique=True, index=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)`,
      'products': `
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Integer)  # in cents
    category_id = Column(Integer, ForeignKey("categories.id"))
    inventory_count = Column(Integer, default=0)`,
      'posts': `
    title = Column(String(255), nullable=False)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    is_published = Column(Boolean, default=False)`,
      'messages': `
    content = Column(Text, nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("chat_rooms.id"))
    message_type = Column(String(50), default="text")`
    };

    return fields[tableName] || `
    name = Column(String(255))
    description = Column(Text)`;
  }

  generateRouter(routerFile, template) {
    const routerName = routerFile.replace('.py', '').replace('_router', '');
    
    return `from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..models.${routerName} import ${this.capitalize(routerName)}

router = APIRouter()

@router.get("/")
async def get_${routerName}(db: Session = Depends(get_db)):
    return {"message": "${routerName} endpoint"}

@router.post("/")
async def create_${routerName}(db: Session = Depends(get_db)):
    return {"message": "Create ${routerName}"}`;
  }

  generateComponent(componentFile, template) {
    const componentName = componentFile.replace('.js', '').split('/').pop();
    
    return `import React from 'react';
import styled from 'styled-components';

const Container = styled.div\`
  padding: 2rem;
\`;

const Title = styled.h1\`
  font-size: 2rem;
  color: #1a202c;
  margin-bottom: 1rem;
\`;

function ${componentName}() {
  return (
    <Container>
      <Title>${componentName}</Title>
      <p>Generated ${componentName} component for ${template.name}</p>
    </Container>
  );
}

export default ${componentName};`;
  }

  generateRequirements(template) {
    const requirements = [
      'fastapi==0.104.1',
      'uvicorn[standard]==0.24.0',
      'sqlalchemy==2.0.23',
      'pymysql==1.1.0',
      'python-multipart==0.0.6',
      'python-jose[cryptography]==3.3.0',
      'passlib[bcrypt]==1.7.4',
      'python-dotenv==1.0.0',
      'pydantic==2.5.0'
    ];

    if (template.features.includes('payment_processing')) {
      requirements.push('stripe==7.8.0');
    }

    if (template.features.includes('real_time_messaging')) {
      requirements.push('websockets==12.0');
    }

    return requirements.join('\n');
  }

  generateDatabaseSchema(template) {
    return template.database.tables.map(table => ({
      table: table,
      fields: this.getTableFields(table)
    }));
  }

  getTableFields(tableName) {
    // Return field definitions for each table type
    const fields = {
      'users': ['id', 'email', 'username', 'password_hash', 'created_at'],
      'products': ['id', 'name', 'description', 'price', 'category_id', 'inventory'],
      'posts': ['id', 'title', 'content', 'author_id', 'published', 'created_at'],
      'messages': ['id', 'content', 'sender_id', 'room_id', 'created_at']
    };

    return fields[tableName] || ['id', 'name', 'created_at'];
  }

  generateDeploymentConfig(template, projectName) {
    return {
      'docker-compose.yml': this.generateDockerCompose(projectName),
      'Dockerfile.frontend': this.generateFrontendDockerfile(),
      'Dockerfile.backend': this.generateBackendDockerfile()
    };
  }

  generateDockerCompose(projectName) {
    return `version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: ${projectName.toLowerCase().replace(/\s+/g, '_')}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://root:password@mysql:3306/${projectName.toLowerCase().replace(/\s+/g, '_')}
    depends_on:
      - mysql

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  mysql_data:`;
  }

  generateFrontendDockerfile() {
    return `FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]`;
  }

  generateBackendDockerfile() {
    return `FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev pkg-config

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`;
  }

  capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  // Get supported technology stacks
  getSupportedTechStacks() {
    return this.techStacks;
  }

  // Get framework recommendations based on project type
  getFrameworkRecommendations(projectType, features = []) {
    const recommendations = {
      primary: {
        frontend: 'react',
        backend: 'fastapi', 
        database: 'mysql',
        reason: 'Balanced stack for most web applications'
      },
      alternatives: []
    };

    // Mobile app recommendations
    if (features.includes('mobile_app') || projectType === 'mobile') {
      recommendations.alternatives.push({
        frontend: 'react_native',
        backend: 'fastapi',
        database: 'postgresql',
        reason: 'Cross-platform mobile development'
      });
      recommendations.alternatives.push({
        frontend: 'flutter',
        backend: 'express',
        database: 'firebase',
        reason: 'High-performance native mobile apps'
      });
    }

    // Enterprise recommendations
    if (features.includes('enterprise') || features.includes('large_scale')) {
      recommendations.alternatives.push({
        frontend: 'angular',
        backend: 'spring_boot',
        database: 'postgresql',
        reason: 'Enterprise-grade with strong typing'
      });
    }

    // Real-time recommendations
    if (features.includes('real_time_updates') || projectType === 'chat') {
      recommendations.alternatives.push({
        frontend: 'react',
        backend: 'express',
        database: 'mongodb',
        reason: 'Optimized for real-time applications'
      });
    }

    // SEO-focused recommendations
    if (features.includes('seo_optimization') || projectType === 'blog') {
      recommendations.primary = {
        frontend: 'nextjs',
        backend: 'fastapi',
        database: 'postgresql',
        reason: 'Server-side rendering for better SEO'
      };
    }

    return recommendations;
  }
}

export default new TemplateService();