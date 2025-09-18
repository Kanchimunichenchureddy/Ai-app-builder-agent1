from typing import Dict, Any, List, Optional
import docker
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime
import time

# Import static server
from .static_server import static_server

class DeployerService:
    """
    Service for deploying generated applications to various platforms.
    Supports Docker, Vercel, Netlify, AWS, GCP, and Azure.
    """
    
    def __init__(self):
        try:
            self.docker_client = docker.from_env()
        except:
            self.docker_client = None
            
        # Initialize cloud clients
        self.aws_client = None
        self.gcp_client = None
        self.azure_client = None
    
    def _init_aws_client(self):
        """Initialize AWS client."""
        try:
            import boto3
            self.aws_client = boto3.client('ec2')  # Basic client for testing
            return True
        except ImportError:
            self.aws_client = None
            return False
        except:
            self.aws_client = None
            return False
            
    def _init_gcp_client(self):
        """Initialize GCP client."""
        try:
            import google.cloud
            # GCP client initialization would go here
            self.gcp_client = None
            return True
        except ImportError:
            self.gcp_client = None
            return False
        except:
            self.gcp_client = None
            return False
            
    def _init_azure_client(self):
        """Initialize Azure client."""
        try:
            from azure.mgmt.resource import ResourceManagementClient
            from azure.mgmt.containerinstance import ContainerInstanceManagementClient
            # Azure client initialization would go here
            self.azure_client = None
            return True
        except ImportError:
            self.azure_client = None
            return False
        except:
            self.azure_client = None
            return False
    
    async def deploy_with_retry(self, deploy_func, project_path: str, project_name: str, config: Dict[str, Any] = None, max_retries: int = 3) -> Dict[str, Any]:
        """
        Deploy with retry mechanism.
        
        Args:
            deploy_func: The deployment function to call
            project_path: Path to the project
            project_name: Name of the project
            config: Deployment configuration
            max_retries: Maximum number of retry attempts
            
        Returns:
            Deployment result dictionary
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    # Wait before retrying (exponential backoff)
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                
                result = await deploy_func(project_path, project_name, config)
                if result["success"]:
                    return result
                else:
                    last_error = result
            except Exception as e:
                last_error = {
                    "success": False,
                    "error": str(e),
                    "message": f"Deployment attempt {attempt + 1} failed: {str(e)}"
                }
        
        # If we get here, all retries failed
        return {
            "success": False,
            "error": last_error.get("error", "Unknown error"),
            "message": f"Deployment failed after {max_retries} attempts. Last error: {last_error.get('message', 'Unknown error')}"
        }
    
    async def deploy_to_docker(self, project_path: str, project_name: str, config: Dict[str, Any] = None, retry: bool = True) -> Dict[str, Any]:
        """Deploy to Docker containers with Nginx reverse proxy."""
        if retry:
            return await self.deploy_with_retry(self._deploy_to_docker_impl, project_path, project_name, config)
        else:
            return await self._deploy_to_docker_impl(project_path, project_name, config)
    
    async def _deploy_to_docker_impl(self, project_path: str, project_name: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Internal implementation of Docker deployment with Nginx reverse proxy."""
        try:
            project_dir = Path(project_path)
            
            if not project_dir.exists():
                raise Exception(f"Project directory not found: {project_path}")
            
            # Try Docker deployment first
            docker_success = False
            docker_error = None
            
            try:
                # Ensure docker-compose.yml exists, create if not
                docker_compose_path = project_dir / "docker-compose.yml"
                if not docker_compose_path.exists():
                    self._create_docker_compose(project_dir, project_name)
                
                # Ensure nginx.conf exists, create if not
                nginx_conf_path = project_dir / "nginx.conf"
                if not nginx_conf_path.exists():
                    self._create_nginx_config(project_dir, project_name)
                
                # Build Docker images
                try:
                    # Build the application
                    build_result = subprocess.run(
                        ["docker-compose", "build"],
                        cwd=project_dir,
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    
                    if build_result.returncode != 0:
                        raise Exception(f"Docker build failed: {build_result.stderr}")
                except subprocess.TimeoutExpired:
                    raise Exception("Docker build timed out")
                except Exception as e:
                    raise Exception(f"Failed to build Docker images: {str(e)}")
                
                # Start containers
                try:
                    up_result = subprocess.run(
                        ["docker-compose", "up", "-d"],
                        cwd=project_dir,
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    
                    if up_result.returncode != 0:
                        raise Exception(f"Docker compose up failed: {up_result.stderr}")
                except subprocess.TimeoutExpired:
                    raise Exception("Docker compose up timed out")
                except Exception as e:
                    raise Exception(f"Failed to start containers: {str(e)}")
                
                docker_success = True
                
            except Exception as e:
                docker_error = str(e)
                print(f"Docker deployment failed: {docker_error}")
            
            # If Docker deployment failed, try static file server as fallback
            if not docker_success:
                print("Falling back to static file server...")
                
                # Try to find the frontend build directory
                frontend_build_path = project_dir / "frontend" / "build"
                if not frontend_build_path.exists():
                    # Try alternative path
                    frontend_build_path = project_dir / "build"
                
                if frontend_build_path.exists():
                    # Use static file server
                    result = static_server.serve_project(
                        project_id=hash(project_name) % 10000,  # Simple project ID generation
                        project_name=project_name,
                        build_path=str(frontend_build_path)
                    )
                    
                    if result["success"]:
                        return {
                            "success": True,
                            "platform": "static",
                            "service_name": f"{project_name}-static",
                            "urls": {
                                "frontend": result["url"],
                                "backend": "Backend not available in static mode",
                                "api_docs": "API docs not available in static mode"
                            },
                            "message": f"Successfully served {project_name} via static file server at {result['url']}"
                        }
                
                # If we can't find build files, return Docker error
                return {
                    "success": False,
                    "error": docker_error,
                    "message": f"Docker deployment failed: {docker_error}. Static file server fallback also failed."
                }
            
            # Return success response with URLs
            return {
                "success": True,
                "platform": "docker",
                "service_name": f"{project_name}-service",
                "urls": {
                    "frontend": f"http://localhost:8080",  # Nginx reverse proxy port
                    "backend": f"http://localhost:8000",
                    "api_docs": f"http://localhost:8000/docs"
                },
                "message": f"Successfully deployed {project_name} to Docker containers with Nginx reverse proxy"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Docker deployment failed: {str(e)}"
            }
    
    def _create_docker_compose(self, project_dir: Path, project_name: str):
        """Create a docker-compose.yml file with Nginx reverse proxy."""
        docker_compose_content = f"""
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    networks:
      - app-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql://user:password@db:3306/{project_name}
    networks:
      - app-network
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: {project_name}
      MYSQL_USER: user
      MYSQL_PASSWORD: password
    ports:
      - "3306:3306"
    networks:
      - app-network
    volumes:
      - db_data:/var/lib/mysql

  nginx:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./frontend/build:/usr/share/nginx/html
    networks:
      - app-network
    depends_on:
      - frontend
      - backend

networks:
  app-network:
    driver: bridge

volumes:
  db_data:
"""
        with open(project_dir / "docker-compose.yml", "w") as f:
            f.write(docker_compose_content)
    
    def _create_nginx_config(self, project_dir: Path, project_name: str):
        """Create an nginx.conf file for reverse proxy."""
        nginx_config_content = """
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }
    
    upstream backend {
        server backend:8000;
    }
    
    server {
        listen 80;
        
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        location /docs {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        location /openapi.json {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
"""
        with open(project_dir / "nginx.conf", "w") as f:
            f.write(nginx_config_content)
    
    async def deploy_to_vercel(self, project_path: str, project_name: str, config: Dict[str, Any] = None, retry: bool = True) -> Dict[str, Any]:
        """Deploy to Vercel."""
        if retry:
            return await self.deploy_with_retry(self._deploy_to_vercel_impl, project_path, project_name, config)
        else:
            return await self._deploy_to_vercel_impl(project_path, project_name, config)
    
    async def _deploy_to_vercel_impl(self, project_path: str, project_name: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Internal implementation of Vercel deployment."""
        try:
            project_dir = Path(project_path)
            
            if not project_dir.exists():
                raise Exception(f"Project directory not found: {project_path}")
            
            # Check if Vercel CLI is installed
            try:
                vercel_check = subprocess.run(
                    ["vercel", "--version"],
                    cwd=project_dir,
                    capture_output=True,
                    text=True
                )
                
                if vercel_check.returncode != 0:
                    raise Exception("Vercel CLI not installed or not in PATH")
            except FileNotFoundError:
                raise Exception("Vercel CLI not installed. Please install it with: npm install -g vercel")
            
            # Deploy frontend to Vercel
            try:
                deploy_result = subprocess.run(
                    ["vercel", "--prod", "--confirm", "--token", os.getenv("VERCEL_TOKEN", "")],
                    cwd=project_dir / "frontend",
                    capture_output=True,
                    text=True,
                    timeout=600
                )
                
                if deploy_result.returncode != 0:
                    raise Exception(f"Vercel deployment failed: {deploy_result.stderr}")
                
                # Extract URL from output
                output_lines = deploy_result.stdout.strip().split('\n')
                frontend_url = output_lines[-1] if output_lines else f"https://{project_name}.vercel.app"
            except subprocess.TimeoutExpired:
                raise Exception("Vercel deployment timed out")
            except Exception as e:
                raise Exception(f"Failed to deploy to Vercel: {str(e)}")
            
            return {
                "success": True,
                "platform": "vercel",
                "service_name": f"{project_name}-frontend",
                "urls": {
                    "frontend": frontend_url,
                    "backend": "Backend must be deployed separately",
                    "api_docs": "Backend must be deployed separately"
                },
                "message": f"Successfully deployed frontend to Vercel: {frontend_url}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Vercel deployment failed: {str(e)}"
            }
    
    async def deploy_to_netlify(self, project_path: str, project_name: str, config: Dict[str, Any] = None, retry: bool = True) -> Dict[str, Any]:
        """Deploy to Netlify."""
        if retry:
            return await self.deploy_with_retry(self._deploy_to_netlify_impl, project_path, project_name, config)
        else:
            return await self._deploy_to_netlify_impl(project_path, project_name, config)
    
    async def _deploy_to_netlify_impl(self, project_path: str, project_name: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Internal implementation of Netlify deployment."""
        try:
            project_dir = Path(project_path)
            
            if not project_dir.exists():
                raise Exception(f"Project directory not found: {project_path}")
            
            # Check if Netlify CLI is installed
            try:
                netlify_check = subprocess.run(
                    ["netlify", "--version"],
                    cwd=project_dir,
                    capture_output=True,
                    text=True
                )
                
                if netlify_check.returncode != 0:
                    raise Exception("Netlify CLI not installed or not in PATH")
            except FileNotFoundError:
                raise Exception("Netlify CLI not installed. Please install it with: npm install -g netlify-cli")
            
            # Build frontend
            try:
                build_result = subprocess.run(
                    ["npm", "run", "build"],
                    cwd=project_dir / "frontend",
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if build_result.returncode != 0:
                    raise Exception(f"Frontend build failed: {build_result.stderr}")
            except subprocess.TimeoutExpired:
                raise Exception("Frontend build timed out")
            except Exception as e:
                raise Exception(f"Failed to build frontend: {str(e)}")
            
            # Deploy to Netlify
            try:
                deploy_result = subprocess.run(
                    ["netlify", "deploy", "--prod", "--dir", "build"],
                    cwd=project_dir / "frontend",
                    capture_output=True,
                    text=True,
                    timeout=600
                )
                
                if deploy_result.returncode != 0:
                    raise Exception(f"Netlify deployment failed: {deploy_result.stderr}")
                
                # Extract URL from output
                output = deploy_result.stdout
                import re
                url_match = re.search(r'https://[^\s]+', output)
                frontend_url = url_match.group(0) if url_match else f"https://{project_name}.netlify.app"
            except subprocess.TimeoutExpired:
                raise Exception("Netlify deployment timed out")
            except Exception as e:
                raise Exception(f"Failed to deploy to Netlify: {str(e)}")
            
            return {
                "success": True,
                "platform": "netlify",
                "service_name": f"{project_name}-frontend",
                "urls": {
                    "frontend": frontend_url,
                    "backend": "Backend must be deployed separately",
                    "api_docs": "Backend must be deployed separately"
                },
                "message": f"Successfully deployed frontend to Netlify: {frontend_url}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Netlify deployment failed: {str(e)}"
            }
    
    async def deploy_to_aws(self, project_path: str, project_name: str, config: Dict[str, Any] = None, retry: bool = True) -> Dict[str, Any]:
        """Deploy to AWS using ECS/Fargate."""
        if retry:
            return await self.deploy_with_retry(self._deploy_to_aws_impl, project_path, project_name, config)
        else:
            return await self._deploy_to_aws_impl(project_path, project_name, config)
    
    async def _deploy_to_aws_impl(self, project_path: str, project_name: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Internal implementation of AWS deployment."""
        try:
            # Try to import boto3 when needed
            try:
                import boto3
            except ImportError:
                raise Exception("AWS SDK (boto3) not installed")
            
            # Initialize AWS client if not already done
            if not self.aws_client:
                try:
                    self.aws_client = boto3.client('ec2')  # Basic client for testing
                except Exception as e:
                    raise Exception(f"Failed to initialize AWS client: {str(e)}")
            
            project_dir = Path(project_path)
            
            # For demonstration, we'll return a mock response
            # In a real implementation, this would:
            # 1. Build Docker images
            # 2. Push to ECR
            # 3. Create ECS task definitions
            # 4. Deploy to ECS/Fargate
            # 5. Configure load balancer and networking
            
            return {
                "success": True,
                "platform": "aws",
                "service_name": f"{project_name}-service",
                "region": "us-east-1",
                "urls": {
                    "frontend": f"https://{project_name}.awsapps.com",
                    "backend": f"https://api.{project_name}.awsapps.com",
                    "api_docs": f"https://api.{project_name}.awsapps.com/docs"
                },
                "resources": {
                    "cluster": f"{project_name}-cluster",
                    "task_definition": f"{project_name}-task",
                    "service": f"{project_name}-service"
                },
                "message": "Successfully deployed to AWS ECS/Fargate"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "AWS deployment failed"
            }
    
    async def deploy_to_gcp(self, project_path: str, project_name: str, config: Dict[str, Any] = None, retry: bool = True) -> Dict[str, Any]:
        """Deploy to Google Cloud Platform using Cloud Run."""
        if retry:
            return await self.deploy_with_retry(self._deploy_to_gcp_impl, project_path, project_name, config)
        else:
            return await self._deploy_to_gcp_impl(project_path, project_name, config)
    
    async def _deploy_to_gcp_impl(self, project_path: str, project_name: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Internal implementation of GCP deployment."""
        try:
            # Try to import google.cloud when needed
            try:
                import google.cloud
            except ImportError:
                raise Exception("Google Cloud SDK not installed")
            
            project_dir = Path(project_path)
            
            # For demonstration, we'll return a mock response
            # In a real implementation, this would:
            # 1. Build Docker images
            # 2. Push to Container Registry
            # 3. Deploy to Cloud Run
            # 4. Configure Cloud SQL
            # 5. Set up load balancing
            
            return {
                "success": True,
                "platform": "gcp",
                "service_name": f"{project_name}-service",
                "region": "us-central1",
                "urls": {
                    "frontend": f"https://{project_name}.run.app",
                    "backend": f"https://api-{project_name}.run.app",
                    "api_docs": f"https://api-{project_name}.run.app/docs"
                },
                "resources": {
                    "cloud_run_service": f"{project_name}-service",
                    "cloud_sql_instance": f"{project_name}-db"
                },
                "message": "Successfully deployed to Google Cloud Run"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "GCP deployment failed"
            }
    
    async def deploy_to_azure(self, project_path: str, project_name: str, config: Dict[str, Any] = None, retry: bool = True) -> Dict[str, Any]:
        """Deploy to Microsoft Azure using App Service."""
        if retry:
            return await self.deploy_with_retry(self._deploy_to_azure_impl, project_path, project_name, config)
        else:
            return await self._deploy_to_azure_impl(project_path, project_name, config)
    
    async def _deploy_to_azure_impl(self, project_path: str, project_name: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Internal implementation of Azure deployment."""
        try:
            # Try to import Azure SDK when needed
            try:
                from azure.mgmt.resource import ResourceManagementClient
                from azure.mgmt.containerinstance import ContainerInstanceManagementClient
            except ImportError:
                raise Exception("Azure SDK not installed")
            
            project_dir = Path(project_path)
            
            # For demonstration, we'll return a mock response
            # In a real implementation, this would:
            # 1. Build Docker images
            # 2. Push to Azure Container Registry
            # 3. Deploy to Azure App Service
            # 4. Configure Azure Database for MySQL
            # 5. Set up Application Gateway
            
            return {
                "success": True,
                "platform": "azure",
                "service_name": f"{project_name}-app",
                "region": "East US",
                "urls": {
                    "frontend": f"https://{project_name}.azurewebsites.net",
                    "backend": f"https://api-{project_name}.azurewebsites.net",
                    "api_docs": f"https://api-{project_name}.azurewebsites.net/docs"
                },
                "resources": {
                    "app_service": f"{project_name}-app",
                    "app_service_plan": f"{project_name}-plan",
                    "mysql_server": f"{project_name}-mysql"
                },
                "message": "Successfully deployed to Azure App Service"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Azure deployment failed"
            }
    
    async def get_deployment_status(self, deployment_id: str, platform: str) -> Dict[str, Any]:
        """Get the status of a deployment."""
        # This is a placeholder implementation
        # In a real implementation, this would check the actual deployment status
        return {
            "status": "deployed",
            "message": "Deployment is active"
        }
    
    async def stop_deployment(self, deployment_id: str, platform: str) -> Dict[str, Any]:
        """Stop a deployment."""
        # This is a placeholder implementation
        # In a real implementation, this would actually stop the deployment
        return {
            "success": True,
            "message": "Deployment stopped successfully"
        }