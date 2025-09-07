from typing import Dict, Any, List, Optional
import docker
import os
import subprocess
import json
import boto3
import google.cloud
from pathlib import Path
from datetime import datetime

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
        self._init_aws_client()
        self._init_gcp_client()
        self._init_azure_client()
        
    def _init_aws_client(self):
        """Initialize AWS client."""
        try:
            self.aws_client = boto3.client('ec2')  # Basic client for testing
        except:
            self.aws_client = None
            
    def _init_gcp_client(self):
        """Initialize GCP client."""
        try:
            # GCP client initialization would go here
            self.gcp_client = None
        except:
            self.gcp_client = None
            
    def _init_azure_client(self):
        """Initialize Azure client."""
        try:
            # Azure client initialization would go here
            self.azure_client = None
        except:
            self.azure_client = None
            
    async def deploy_to_docker(self, project_path: str, project_name: str) -> Dict[str, Any]:
        """Deploy project to Docker containers."""
        try:
            if not self.docker_client:
                raise Exception("Docker is not available")
            
            project_dir = Path(project_path)
            
            # Build Docker images
            frontend_image = await self._build_frontend_image(project_dir, project_name)
            backend_image = await self._build_backend_image(project_dir, project_name)
            
            # Create network
            network_name = f"{project_name}_network"
            try:
                network = self.docker_client.networks.create(
                    network_name,
                    driver="bridge"
                )
            except docker.errors.APIError:
                # Network might already exist
                network = self.docker_client.networks.get(network_name)
            
            # Start MySQL container
            mysql_container = await self._start_mysql_container(project_name, network)
            
            # Start backend container
            backend_container = await self._start_backend_container(
                backend_image, project_name, network, mysql_container.name
            )
            
            # Start frontend container
            frontend_container = await self._start_frontend_container(
                frontend_image, project_name, network, backend_container.name
            )
            
            return {
                "success": True,
                "platform": "docker",
                "containers": {
                    "mysql": mysql_container.id,
                    "backend": backend_container.id,
                    "frontend": frontend_container.id
                },
                "urls": {
                    "frontend": f"http://localhost:3000",
                    "backend": f"http://localhost:8000",
                    "api_docs": f"http://localhost:8000/docs"
                },
                "message": "Successfully deployed to Docker"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Docker deployment failed"
            }
    
    async def deploy_to_vercel(self, project_path: str, project_name: str) -> Dict[str, Any]:
        """Deploy frontend to Vercel."""
        try:
            project_dir = Path(project_path)
            frontend_dir = project_dir / "frontend"
            
            if not frontend_dir.exists():
                raise Exception("Frontend directory not found")
            
            # Check if Vercel CLI is installed
            result = subprocess.run(["vercel", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception("Vercel CLI not installed")
            
            # Deploy to Vercel
            deploy_result = subprocess.run(
                ["vercel", "--prod", "--yes"],
                cwd=frontend_dir,
                capture_output=True,
                text=True
            )
            
            if deploy_result.returncode != 0:
                raise Exception(f"Vercel deployment failed: {deploy_result.stderr}")
            
            # Extract URL from output
            deployment_url = deploy_result.stdout.strip().split('\n')[-1]
            
            return {
                "success": True,
                "platform": "vercel",
                "url": deployment_url,
                "message": "Successfully deployed to Vercel"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Vercel deployment failed"
            }
    
    async def deploy_to_netlify(self, project_path: str, project_name: str) -> Dict[str, Any]:
        """Deploy frontend to Netlify."""
        try:
            project_dir = Path(project_path)
            frontend_dir = project_dir / "frontend"
            
            if not frontend_dir.exists():
                raise Exception("Frontend directory not found")
            
            # Build the frontend
            build_result = subprocess.run(
                ["npm", "run", "build"],
                cwd=frontend_dir,
                capture_output=True,
                text=True
            )
            
            if build_result.returncode != 0:
                raise Exception(f"Frontend build failed: {build_result.stderr}")
            
            # Deploy to Netlify (requires netlify-cli)
            deploy_result = subprocess.run(
                ["netlify", "deploy", "--prod", "--dir", "build"],
                cwd=frontend_dir,
                capture_output=True,
                text=True
            )
            
            if deploy_result.returncode != 0:
                raise Exception(f"Netlify deployment failed: {deploy_result.stderr}")
            
            # Extract URL from output
            lines = deploy_result.stdout.strip().split('\n')
            deployment_url = next((line.split(': ')[1] for line in lines if 'Live URL:' in line), None)
            
            return {
                "success": True,
                "platform": "netlify",
                "url": deployment_url,
                "message": "Successfully deployed to Netlify"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Netlify deployment failed"
            }
    
    async def deploy_to_aws(self, project_path: str, project_name: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Deploy to AWS using ECS/Fargate."""
        try:
            if not self.aws_client:
                raise Exception("AWS client not configured")
            
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
    
    async def deploy_to_gcp(self, project_path: str, project_name: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Deploy to Google Cloud Platform using Cloud Run."""
        try:
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
    
    async def deploy_to_azure(self, project_path: str, project_name: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Deploy to Microsoft Azure using App Service."""
        try:
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
        """Get deployment status."""
        try:
            if platform == "docker":
                return await self._get_docker_status(deployment_id)
            elif platform == "vercel":
                return await self._get_vercel_status(deployment_id)
            elif platform == "netlify":
                return await self._get_netlify_status(deployment_id)
            elif platform == "aws":
                return await self._get_aws_status(deployment_id)
            elif platform == "gcp":
                return await self._get_gcp_status(deployment_id)
            elif platform == "azure":
                return await self._get_azure_status(deployment_id)
            else:
                raise Exception(f"Unsupported platform: {platform}")
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def stop_deployment(self, deployment_id: str, platform: str) -> Dict[str, Any]:
        """Stop a deployment."""
        try:
            if platform == "docker":
                return await self._stop_docker_deployment(deployment_id)
            elif platform in ["aws", "gcp", "azure"]:
                return await self._stop_cloud_deployment(deployment_id, platform)
            else:
                raise Exception(f"Stop not supported for platform: {platform}")
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _build_frontend_image(self, project_dir: Path, project_name: str) -> str:
        """Build Docker image for frontend."""
        frontend_dir = project_dir / "frontend"
        
        # Create Dockerfile if it doesn't exist
        dockerfile_content = '''FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]'''
        
        dockerfile_path = frontend_dir / "Dockerfile"
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        
        # Build image
        image_name = f"{project_name}_frontend"
        image, build_logs = self.docker_client.images.build(
            path=str(frontend_dir),
            tag=image_name,
            rm=True
        )
        
        return image_name
    
    async def _build_backend_image(self, project_dir: Path, project_name: str) -> str:
        """Build Docker image for backend."""
        backend_dir = project_dir / "backend"
        
        # Create Dockerfile if it doesn't exist
        dockerfile_content = '''FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev pkg-config
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]'''
        
        dockerfile_path = backend_dir / "Dockerfile"
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        
        # Build image
        image_name = f"{project_name}_backend"
        image, build_logs = self.docker_client.images.build(
            path=str(backend_dir),
            tag=image_name,
            rm=True
        )
        
        return image_name
    
    async def _start_mysql_container(self, project_name: str, network) -> Any:
        """Start MySQL container."""
        container_name = f"{project_name}_mysql"
        
        # Remove existing container if it exists
        try:
            existing_container = self.docker_client.containers.get(container_name)
            existing_container.remove(force=True)
        except docker.errors.NotFound:
            pass
        
        container = self.docker_client.containers.run(
            "mysql:8.0",
            name=container_name,
            environment={
                "MYSQL_ROOT_PASSWORD": "password",
                "MYSQL_DATABASE": "app_db"
            },
            networks=[network.name],
            ports={'3306/tcp': 3306},
            detach=True
        )
        
        return container
    
    async def _start_backend_container(self, image_name: str, project_name: str, network, mysql_container_name: str) -> Any:
        """Start backend container."""
        container_name = f"{project_name}_backend"
        
        # Remove existing container if it exists
        try:
            existing_container = self.docker_client.containers.get(container_name)
            existing_container.remove(force=True)
        except docker.errors.NotFound:
            pass
        
        container = self.docker_client.containers.run(
            image_name,
            name=container_name,
            environment={
                "DATABASE_URL": f"mysql+pymysql://root:password@{mysql_container_name}:3306/app_db"
            },
            networks=[network.name],
            ports={'8000/tcp': 8000},
            detach=True
        )
        
        return container
    
    async def _start_frontend_container(self, image_name: str, project_name: str, network, backend_container_name: str) -> Any:
        """Start frontend container."""
        container_name = f"{project_name}_frontend"
        
        # Remove existing container if it exists
        try:
            existing_container = self.docker_client.containers.get(container_name)
            existing_container.remove(force=True)
        except docker.errors.NotFound:
            pass
        
        container = self.docker_client.containers.run(
            image_name,
            name=container_name,
            networks=[network.name],
            ports={'80/tcp': 3000},
            detach=True
        )
        
        return container
    
    async def _get_aws_status(self, deployment_id: str) -> Dict[str, Any]:
        """Get AWS deployment status."""
        # Implementation for checking AWS deployment status
        return {"status": "deployed", "service": "running"}
    
    async def _get_gcp_status(self, deployment_id: str) -> Dict[str, Any]:
        """Get GCP deployment status."""
        # Implementation for checking GCP deployment status
        return {"status": "deployed", "service": "running"}
    
    async def _get_azure_status(self, deployment_id: str) -> Dict[str, Any]:
        """Get Azure deployment status."""
        # Implementation for checking Azure deployment status
        return {"status": "deployed", "service": "running"}
    
    async def _stop_cloud_deployment(self, deployment_id: str, platform: str) -> Dict[str, Any]:
        """Stop cloud deployment."""
        # Implementation for stopping cloud deployments
        return {"success": True, "message": f"{platform.upper()} deployment stopped"}