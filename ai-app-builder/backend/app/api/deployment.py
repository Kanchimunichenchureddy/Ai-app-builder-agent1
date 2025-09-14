from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import List, Dict, Any
import json
from sqlalchemy.orm import Session

# Fix the import paths - use absolute imports
from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.models.project import Project
from app.models.deployment import Deployment, DeploymentStatus, DeploymentPlatform
from app.services.deployer import DeployerService

router = APIRouter()
security = HTTPBearer()
deployer = DeployerService()

async def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)) -> User:
    """Get current authenticated user."""
    payload = verify_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.post("/deploy/{project_id}")
async def deploy_project(
    project_id: int,
    deployment_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deploy a project to specified platform."""
    try:
        # Get project
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.owner_id == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        platform = deployment_data.get("platform")
        deployment_name = deployment_data.get("name", f"{project.name}-deployment")
        
        if not platform:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Platform is required"
            )
        
        try:
            platform_enum = DeploymentPlatform(platform)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported platform: {platform}"
            )
        
        # Create deployment record
        deployment = Deployment(
            name=deployment_name,
            platform=platform_enum,
            status=DeploymentStatus.PENDING,
            project_id=project_id,
            user_id=current_user.id,
            config=deployment_data.get("config", {}),
            environment_variables=deployment_data.get("env_vars", {})
        )
        
        db.add(deployment)
        db.commit()
        db.refresh(deployment)
        
        # Start deployment process
        deployment.status = DeploymentStatus.BUILDING
        db.commit()
        
        # Deploy based on platform
        if platform == "docker":
            result = await deployer.deploy_to_docker(project.project_path, project.name, retry=True)
        elif platform == "vercel":
            result = await deployer.deploy_to_vercel(project.project_path, project.name, retry=True)
        elif platform == "netlify":
            result = await deployer.deploy_to_netlify(project.project_path, project.name, retry=True)
        elif platform == "aws":
            result = await deployer.deploy_to_aws(project.project_path, project.name, deployment.config, retry=True)
        elif platform == "gcp":
            result = await deployer.deploy_to_gcp(project.project_path, project.name, deployment.config, retry=True)
        elif platform == "azure":
            result = await deployer.deploy_to_azure(project.project_path, project.name, deployment.config, retry=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Platform {platform} not yet implemented"
            )
        
        # Update deployment based on result
        if result["success"]:
            deployment.status = DeploymentStatus.DEPLOYED
            deployment.url = result.get("url")
            deployment.api_url = result.get("urls", {}).get("backend")
            deployment.deployment_logs = result.get("message", "")
        else:
            deployment.status = DeploymentStatus.FAILED
            deployment.error_message = result.get("error", "Unknown error")
        
        db.commit()
        
        return {
            "success": result["success"],
            "deployment": {
                "id": deployment.id,
                "name": deployment.name,
                "platform": deployment.platform,
                "status": deployment.status,
                "url": deployment.url,
                "api_url": deployment.api_url
            },
            "result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Deployment failed: {str(e)}"
        )

@router.get("/deployments/{project_id}")
async def get_project_deployments(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all deployments for a project."""
    # Verify project ownership
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    deployments = db.query(Deployment).filter(
        Deployment.project_id == project_id
    ).order_by(Deployment.created_at.desc()).all()
    
    return {
        "success": True,
        "deployments": [
            {
                "id": deployment.id,
                "name": deployment.name,
                "platform": deployment.platform,
                "status": deployment.status,
                "url": deployment.url,
                "api_url": deployment.api_url,
                "created_at": deployment.created_at.isoformat(),
                "deployed_at": deployment.deployed_at.isoformat() if deployment.deployed_at else None,
                "error_message": deployment.error_message
            }
            for deployment in deployments
        ]
    }

@router.get("/deployment/{deployment_id}/status")
async def get_deployment_status(
    deployment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get deployment status."""
    deployment = db.query(Deployment).filter(
        Deployment.id == deployment_id,
        Deployment.user_id == current_user.id
    ).first()
    
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    
    # Get live status from platform
    live_status = await deployer.get_deployment_status(
        str(deployment_id), 
        deployment.platform.value
    )
    
    return {
        "success": True,
        "deployment": {
            "id": deployment.id,
            "name": deployment.name,
            "platform": deployment.platform,
            "status": deployment.status,
            "url": deployment.url,
            "api_url": deployment.api_url,
            "created_at": deployment.created_at.isoformat(),
            "live_status": live_status
        }
    }

@router.post("/deployment/{deployment_id}/stop")
async def stop_deployment(
    deployment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Stop a deployment."""
    deployment = db.query(Deployment).filter(
        Deployment.id == deployment_id,
        Deployment.user_id == current_user.id
    ).first()
    
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    
    # Stop deployment
    result = await deployer.stop_deployment(
        str(deployment_id),
        deployment.platform.value
    )
    
    if result["success"]:
        deployment.status = DeploymentStatus.STOPPED
        db.commit()
    
    return {
        "success": result["success"],
        "message": result.get("message", "Deployment stopped"),
        "deployment_id": deployment_id
    }

@router.delete("/deployment/{deployment_id}")
async def delete_deployment(
    deployment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a deployment."""
    deployment = db.query(Deployment).filter(
        Deployment.id == deployment_id,
        Deployment.user_id == current_user.id
    ).first()
    
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    
    # Stop deployment if it's running
    if deployment.status in [DeploymentStatus.DEPLOYED, DeploymentStatus.BUILDING]:
        await deployer.stop_deployment(
            str(deployment_id),
            deployment.platform.value
        )
    
    db.delete(deployment)
    db.commit()
    
    return {
        "success": True,
        "message": "Deployment deleted successfully"
    }

@router.get("/platforms")
async def get_supported_platforms():
    """Get supported deployment platforms."""
    return {
        "success": True,
        "platforms": [
            {
                "id": "docker",
                "name": "Docker",
                "description": "Deploy using Docker containers",
                "features": ["Full-stack deployment", "Local development", "Easy scaling"],
                "requirements": ["Docker installed"]
            },
            {
                "id": "vercel",
                "name": "Vercel",
                "description": "Deploy frontend to Vercel",
                "features": ["Fast CDN", "Automatic HTTPS", "Git integration"],
                "requirements": ["Vercel account", "Vercel CLI"]
            },
            {
                "id": "netlify",
                "name": "Netlify",
                "description": "Deploy frontend to Netlify",
                "features": ["JAMstack optimized", "Form handling", "Split testing"],
                "requirements": ["Netlify account", "Netlify CLI"]
            },
            {
                "id": "aws",
                "name": "AWS",
                "description": "Deploy to Amazon Web Services",
                "features": ["Scalable infrastructure", "Global reach", "Multiple services", "ECS/Fargate", "Auto-scaling"],
                "requirements": ["AWS account", "AWS CLI", "Docker"],
                "status": "Available"
            },
            {
                "id": "gcp",
                "name": "Google Cloud",
                "description": "Deploy to Google Cloud Platform",
                "features": ["Machine learning integration", "Global network", "Kubernetes", "Cloud Run", "AutoML"],
                "requirements": ["GCP account", "gcloud CLI", "Docker"],
                "status": "Available"
            },
            {
                "id": "azure",
                "name": "Microsoft Azure",
                "description": "Deploy to Microsoft Azure",
                "features": ["Enterprise integration", "AI services", "DevOps", "App Service", "Functions"],
                "requirements": ["Azure account", "Azure CLI", "Docker"],
                "status": "Available"
            }
        ]
    }