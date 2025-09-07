from typing import Dict, List, Optional, Any
import json
import os
from pathlib import Path
from .integrations.openai_service import OpenAIService
from .integrations.gemini_service import GeminiService

class FrameworkGenerator:
    """
    Advanced code generator supporting multiple frontend and backend frameworks.
    Enables building applications with various technology stacks.
    """
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.gemini_service = GeminiService()
        
        # Supported frameworks
        self.frontend_frameworks = {
            'react': {
                'name': 'React.js',
                'description': 'Modern React with hooks and context',
                'dependencies': ['react', 'react-dom', 'react-router-dom', 'axios'],
                'dev_dependencies': ['@vitejs/plugin-react', 'vite']
            },
            'nextjs': {
                'name': 'Next.js',
                'description': 'Full-stack React framework with SSR/SSG',
                'dependencies': ['next', 'react', 'react-dom'],
                'features': ['ssr', 'ssg', 'api_routes', 'image_optimization']
            },
            'vue': {
                'name': 'Vue.js 3',
                'description': 'Progressive JavaScript framework',
                'dependencies': ['vue', 'vue-router', 'pinia', 'axios'],
                'dev_dependencies': ['@vitejs/plugin-vue', 'vite']
            },
            'angular': {
                'name': 'Angular',
                'description': 'Enterprise-grade TypeScript framework',
                'dependencies': ['@angular/core', '@angular/common', '@angular/router'],
                'features': ['typescript', 'dependency_injection', 'cli']
            },
            'react_native': {
                'name': 'React Native',
                'description': 'Cross-platform mobile development',
                'dependencies': ['react', 'react-native', '@react-navigation/native'],
                'platforms': ['ios', 'android']
            },
            'flutter': {
                'name': 'Flutter',
                'description': 'Cross-platform app development with Dart',
                'language': 'dart',
                'platforms': ['ios', 'android', 'web', 'desktop']
            }
        }
        
        self.backend_frameworks = {
            'fastapi': {
                'name': 'FastAPI',
                'language': 'python',
                'description': 'High-performance async Python API framework',
                'dependencies': ['fastapi', 'uvicorn', 'sqlalchemy', 'pydantic']
            },
            'express': {
                'name': 'Express.js',
                'language': 'javascript',
                'description': 'Fast Node.js web framework',
                'dependencies': ['express', 'cors', 'helmet', 'morgan']
            },
            'nestjs': {
                'name': 'NestJS',
                'language': 'typescript',
                'description': 'Progressive Node.js framework',
                'dependencies': ['@nestjs/core', '@nestjs/common', '@nestjs/platform-express']
            },
            'django': {
                'name': 'Django',
                'language': 'python',
                'description': 'High-level Python web framework',
                'dependencies': ['django', 'djangorestframework', 'django-cors-headers']
            },
            'spring_boot': {
                'name': 'Spring Boot',
                'language': 'java',
                'description': 'Enterprise Java framework',
                'dependencies': ['spring-boot-starter-web', 'spring-boot-starter-data-jpa']
            },
            'gin': {
                'name': 'Gin',
                'language': 'go',
                'description': 'Lightweight Go web framework',
                'dependencies': ['github.com/gin-gonic/gin']
            }
        }
        
        self.databases = {
            'mysql': {'type': 'relational', 'features': ['transactions', 'joins', 'acid']},
            'postgresql': {'type': 'relational', 'features': ['json', 'full_text', 'geo']},
            'mongodb': {'type': 'document', 'features': ['flexible_schema', 'aggregation']},
            'redis': {'type': 'key_value', 'features': ['caching', 'sessions', 'pub_sub']},
            'sqlite': {'type': 'relational', 'features': ['embedded', 'serverless']},
            'firebase': {'type': 'cloud', 'features': ['realtime', 'auth', 'hosting']}
        }
    
    async def generate_project_with_frameworks(
        self, 
        frontend_framework: str,
        backend_framework: str,
        database: str,
        analysis: Dict[str, Any],
        project_name: str
    ) -> Dict[str, Any]:
        """
        Generate complete project with specified frameworks.
        """
        # Validate framework support
        if frontend_framework not in self.frontend_frameworks:
            raise ValueError(f"Frontend framework '{frontend_framework}' not supported")
        if backend_framework not in self.backend_frameworks:
            raise ValueError(f"Backend framework '{backend_framework}' not supported")
        if database not in self.databases:
            raise ValueError(f"Database '{database}' not supported")
        
        project_data = {
            "name": project_name,
            "type": analysis.get("project_type", "web_app"),
            "tech_stack": {
                "frontend": frontend_framework,
                "backend": backend_framework,
                "database": database
            },
            "framework_config": {
                "frontend": self.frontend_frameworks[frontend_framework],
                "backend": self.backend_frameworks[backend_framework],
                "database": self.databases[database]
            },
            "files": {},
            "structure": {}
        }
        
        # Generate framework-specific structure
        project_data["structure"] = await self._generate_framework_structure(
            frontend_framework, backend_framework, analysis
        )
        
        # Generate framework-specific files
        project_data["files"] = await self._generate_framework_files(
            frontend_framework, backend_framework, database, analysis, project_data["structure"]
        )
        
        return project_data
    
    async def _generate_framework_structure(
        self, 
        frontend: str, 
        backend: str, 
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate project structure based on frameworks."""
        structure = {}
        
        # Frontend structure
        if frontend == 'react':
            structure["frontend"] = self._get_react_structure()
        elif frontend == 'nextjs':
            structure["frontend"] = self._get_nextjs_structure()
        elif frontend == 'vue':
            structure["frontend"] = self._get_vue_structure()
        elif frontend == 'angular':
            structure["frontend"] = self._get_angular_structure()
        elif frontend == 'react_native':
            structure["mobile"] = self._get_react_native_structure()
        elif frontend == 'flutter':
            structure["mobile"] = self._get_flutter_structure()
        
        # Backend structure
        if backend == 'fastapi':
            structure["backend"] = self._get_fastapi_structure()
        elif backend == 'express':
            structure["backend"] = self._get_express_structure()
        elif backend == 'nestjs':
            structure["backend"] = self._get_nestjs_structure()
        elif backend == 'django':
            structure["backend"] = self._get_django_structure()
        elif backend == 'spring_boot':
            structure["backend"] = self._get_spring_boot_structure()
        elif backend == 'gin':
            structure["backend"] = self._get_gin_structure()
        
        return structure
    
    async def _generate_framework_files(
        self,
        frontend: str,
        backend: str,
        database: str,
        analysis: Dict[str, Any],
        structure: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate all files for the specified frameworks."""
        files = {}
        
        # Generate frontend files
        if frontend == 'react':
            frontend_files = await self._generate_react_files(analysis, structure.get("frontend", {}))
        elif frontend == 'nextjs':
            frontend_files = await self._generate_nextjs_files(analysis, structure.get("frontend", {}))
        elif frontend == 'vue':
            frontend_files = await self._generate_vue_files(analysis, structure.get("frontend", {}))
        elif frontend == 'angular':
            frontend_files = await self._generate_angular_files(analysis, structure.get("frontend", {}))
        elif frontend == 'react_native':
            frontend_files = await self._generate_react_native_files(analysis, structure.get("mobile", {}))
        elif frontend == 'flutter':
            frontend_files = await self._generate_flutter_files(analysis, structure.get("mobile", {}))
        else:
            frontend_files = {}
        
        files.update(frontend_files)
        
        # Generate backend files
        if backend == 'fastapi':
            backend_files = await self._generate_fastapi_files(analysis, structure.get("backend", {}))
        elif backend == 'express':
            backend_files = await self._generate_express_files(analysis, structure.get("backend", {}))
        elif backend == 'nestjs':
            backend_files = await self._generate_nestjs_files(analysis, structure.get("backend", {}))
        elif backend == 'django':
            backend_files = await self._generate_django_files(analysis, structure.get("backend", {}))
        elif backend == 'spring_boot':
            backend_files = await self._generate_spring_boot_files(analysis, structure.get("backend", {}))
        elif backend == 'gin':
            backend_files = await self._generate_gin_files(analysis, structure.get("backend", {}))
        else:
            backend_files = {}
        
        files.update(backend_files)
        
        # Generate database files
        database_files = await self._generate_database_files(database, analysis)
        files.update(database_files)
        
        # Generate deployment files
        deployment_files = await self._generate_deployment_files(frontend, backend, database)
        files.update(deployment_files)
        
        return files
    
    # Structure definitions
    def _get_react_structure(self) -> Dict[str, Any]:
        return {
            "src": {
                "components": {"ui": {}, "layout": {}, "forms": {}},
                "pages": {},
                "services": {},
                "hooks": {},
                "context": {},
                "utils": {},
                "styles": {},
                "assets": {"images": {}, "icons": {}}
            },
            "public": {}
        }
    
    def _get_nextjs_structure(self) -> Dict[str, Any]:
        return {
            "pages": {"api": {}},
            "components": {"ui": {}, "layout": {}},
            "lib": {},
            "styles": {},
            "public": {},
            "utils": {}
        }
    
    def _get_vue_structure(self) -> Dict[str, Any]:
        return {
            "src": {
                "components": {"ui": {}, "layout": {}},
                "views": {},
                "router": {},
                "store": {},
                "composables": {},
                "utils": {},
                "assets": {}
            },
            "public": {}
        }
    
    def _get_angular_structure(self) -> Dict[str, Any]:
        return {
            "src": {
                "app": {
                    "components": {},
                    "services": {},
                    "guards": {},
                    "interceptors": {},
                    "models": {},
                    "modules": {}
                },
                "assets": {},
                "environments": {}
            }
        }
    
    def _get_react_native_structure(self) -> Dict[str, Any]:
        return {
            "src": {
                "components": {},
                "screens": {},
                "navigation": {},
                "services": {},
                "utils": {},
                "assets": {"images": {}, "fonts": {}}
            },
            "android": {},
            "ios": {}
        }
    
    def _get_flutter_structure(self) -> Dict[str, Any]:
        return {
            "lib": {
                "screens": {},
                "widgets": {},
                "services": {},
                "models": {},
                "utils": {}
            },
            "assets": {"images": {}, "fonts": {}},
            "android": {},
            "ios": {}
        }
    
    def _get_fastapi_structure(self) -> Dict[str, Any]:
        return {
            "app": {
                "api": {"v1": {}},
                "core": {},
                "models": {},
                "schemas": {},
                "services": {},
                "utils": {}
            }
        }
    
    def _get_express_structure(self) -> Dict[str, Any]:
        return {
            "src": {
                "controllers": {},
                "middlewares": {},
                "models": {},
                "routes": {},
                "services": {},
                "utils": {},
                "config": {}
            }
        }
    
    def _get_nestjs_structure(self) -> Dict[str, Any]:
        return {
            "src": {
                "modules": {},
                "controllers": {},
                "services": {},
                "guards": {},
                "interceptors": {},
                "dto": {},
                "entities": {}
            }
        }
    
    def _get_django_structure(self) -> Dict[str, Any]:
        return {
            "project": {
                "apps": {},
                "settings": {},
                "urls": {}
            },
            "requirements": {}
        }
    
    def _get_spring_boot_structure(self) -> Dict[str, Any]:
        return {
            "src": {
                "main": {
                    "java": {"com": {"app": {
                        "controller": {},
                        "service": {},
                        "repository": {},
                        "model": {},
                        "config": {}
                    }}},
                    "resources": {}
                }
            }
        }
    
    def _get_gin_structure(self) -> Dict[str, Any]:
        return {
            "cmd": {},
            "internal": {
                "handlers": {},
                "services": {},
                "models": {},
                "middleware": {}
            },
            "pkg": {}
        }
    
    # File generation methods (simplified - actual implementation would use AI)
    async def _generate_react_files(self, analysis: Dict[str, Any], structure: Dict[str, Any]) -> Dict[str, str]:
        """Generate React.js files."""
        return {
            "frontend/package.json": self._get_react_package_json(),
            "frontend/src/App.js": self._get_react_app_js(analysis),
            "frontend/src/index.js": self._get_react_index_js(),
            "frontend/vite.config.js": self._get_vite_config(),
            "frontend/index.html": self._get_react_html()
        }
    
    async def _generate_nextjs_files(self, analysis: Dict[str, Any], structure: Dict[str, Any]) -> Dict[str, str]:
        """Generate Next.js files."""
        return {
            "frontend/package.json": self._get_nextjs_package_json(),
            "frontend/pages/_app.js": self._get_nextjs_app(),
            "frontend/pages/index.js": self._get_nextjs_index(analysis),
            "frontend/next.config.js": self._get_nextjs_config()
        }
    
    async def _generate_vue_files(self, analysis: Dict[str, Any], structure: Dict[str, Any]) -> Dict[str, str]:
        """Generate Vue.js files."""
        return {
            "frontend/package.json": self._get_vue_package_json(),
            "frontend/src/App.vue": self._get_vue_app(analysis),
            "frontend/src/main.js": self._get_vue_main(),
            "frontend/vite.config.js": self._get_vue_vite_config()
        }
    
    async def _generate_angular_files(self, analysis: Dict[str, Any], structure: Dict[str, Any]) -> Dict[str, str]:
        """Generate Angular files."""
        return {
            "frontend/package.json": self._get_angular_package_json(),
            "frontend/src/app/app.component.ts": self._get_angular_app_component(analysis),
            "frontend/src/main.ts": self._get_angular_main(),
            "frontend/angular.json": self._get_angular_config()
        }
    
    async def _generate_react_native_files(self, analysis: Dict[str, Any], structure: Dict[str, Any]) -> Dict[str, str]:
        """Generate React Native files."""
        return {
            "mobile/package.json": self._get_react_native_package_json(),
            "mobile/App.js": self._get_react_native_app(analysis),
            "mobile/index.js": self._get_react_native_index(),
            "mobile/metro.config.js": self._get_metro_config()
        }
    
    async def _generate_flutter_files(self, analysis: Dict[str, Any], structure: Dict[str, Any]) -> Dict[str, str]:
        """Generate Flutter files."""
        return {
            "mobile/pubspec.yaml": self._get_flutter_pubspec(),
            "mobile/lib/main.dart": self._get_flutter_main(analysis),
            "mobile/lib/app.dart": self._get_flutter_app()
        }
    
    async def _generate_fastapi_files(self, analysis: Dict[str, Any], structure: Dict[str, Any]) -> Dict[str, str]:
        """Generate FastAPI files."""
        return {
            "backend/requirements.txt": self._get_fastapi_requirements(),
            "backend/main.py": self._get_fastapi_main(analysis),
            "backend/app/core/config.py": self._get_fastapi_config(),
            "backend/app/api/v1/router.py": self._get_fastapi_router(analysis)
        }
    
    async def _generate_express_files(self, analysis: Dict[str, Any], structure: Dict[str, Any]) -> Dict[str, str]:
        """Generate Express.js files."""
        return {
            "backend/package.json": self._get_express_package_json(),
            "backend/src/app.js": self._get_express_app(analysis),
            "backend/src/server.js": self._get_express_server(),
            "backend/src/routes/index.js": self._get_express_routes(analysis)
        }
    
    async def _generate_nestjs_files(self, analysis: Dict[str, Any], structure: Dict[str, Any]) -> Dict[str, str]:
        """Generate NestJS files."""
        return {
            "backend/package.json": self._get_nestjs_package_json(),
            "backend/src/main.ts": self._get_nestjs_main(),
            "backend/src/app.module.ts": self._get_nestjs_app_module(analysis)
        }
    
    async def _generate_django_files(self, analysis: Dict[str, Any], structure: Dict[str, Any]) -> Dict[str, str]:
        """Generate Django files."""
        return {
            "backend/requirements.txt": self._get_django_requirements(),
            "backend/manage.py": self._get_django_manage(),
            "backend/project/settings.py": self._get_django_settings(analysis)
        }
    
    async def _generate_spring_boot_files(self, analysis: Dict[str, Any], structure: Dict[str, Any]) -> Dict[str, str]:
        """Generate Spring Boot files."""
        return {
            "backend/pom.xml": self._get_spring_boot_pom(),
            "backend/src/main/java/com/app/Application.java": self._get_spring_boot_main(),
            "backend/src/main/resources/application.yml": self._get_spring_boot_config(analysis)
        }
    
    async def _generate_gin_files(self, analysis: Dict[str, Any], structure: Dict[str, Any]) -> Dict[str, str]:
        """Generate Gin (Go) files."""
        return {
            "backend/go.mod": self._get_go_mod(),
            "backend/main.go": self._get_gin_main(analysis),
            "backend/internal/handlers/handler.go": self._get_gin_handler(analysis)
        }
    
    async def _generate_database_files(self, database: str, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate database configuration files."""
        files = {}
        
        if database == 'mysql':
            files["database/init.sql"] = self._get_mysql_init(analysis)
        elif database == 'postgresql':
            files["database/init.sql"] = self._get_postgresql_init(analysis)
        elif database == 'mongodb':
            files["database/init.js"] = self._get_mongodb_init(analysis)
        
        return files
    
    async def _generate_deployment_files(self, frontend: str, backend: str, database: str) -> Dict[str, str]:
        """Generate deployment configuration files."""
        return {
            "docker-compose.yml": self._get_docker_compose(frontend, backend, database),
            "Dockerfile.frontend": self._get_frontend_dockerfile(frontend),
            "Dockerfile.backend": self._get_backend_dockerfile(backend),
            ".github/workflows/deploy.yml": self._get_github_actions(frontend, backend)
        }
    
    # Simplified file templates (actual implementation would use more sophisticated generation)
    def _get_react_package_json(self) -> str:
        return json.dumps({
            "name": "react-app",
            "version": "1.0.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.8.0",
                "axios": "^1.3.0"
            },
            "devDependencies": {
                "@vitejs/plugin-react": "^3.1.0",
                "vite": "^4.1.0"
            }
        }, indent=2)
    
    def _get_react_app_js(self, analysis: Dict[str, Any]) -> str:
        return '''import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>AI Generated App</h1>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

const Home = () => {
  return (
    <div>
      <h2>Welcome to your AI generated application!</h2>
    </div>
  );
};

export default App;'''
    
    def _get_react_index_js(self) -> str:
        return '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);'''
    
    def _get_vite_config(self) -> str:
        return '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000
  }
})'''
    
    def _get_react_html(self) -> str:
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Generated App</title>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/src/index.js"></script>
</body>
</html>'''
    
    def _get_fastapi_requirements(self) -> str:
        return '''fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pymysql==1.1.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0'''
    
    def _get_fastapi_main(self, analysis: Dict[str, Any]) -> str:
        return '''from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title="AI Generated API",
    description="Generated by AI App Builder",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "AI Generated API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)'''
    
    def _get_docker_compose(self, frontend: str, backend: str, database: str) -> str:
        return f'''version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: ../Dockerfile.frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: ../Dockerfile.backend
    ports:
      - "8000:8000"
    depends_on:
      - database
    environment:
      - DATABASE_URL={database}://user:password@database:3306/appdb

  database:
    image: {database}:latest
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=appdb
      - MYSQL_USER=user
      - MYSQL_PASSWORD=password
    ports:
      - "3306:3306"
    volumes:
      - database_data:/var/lib/mysql

volumes:
  database_data:'''

    # Additional helper methods for other frameworks...
    # (Implementation continues with similar patterns for other frameworks)
    
    def get_supported_frameworks(self) -> Dict[str, Any]:
        """Get all supported frameworks and their configurations."""
        return {
            "frontend": self.frontend_frameworks,
            "backend": self.backend_frameworks,
            "databases": self.databases
        }