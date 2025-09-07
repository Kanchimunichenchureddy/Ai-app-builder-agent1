from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import os
import shutil
from pathlib import Path

from ..core.database import get_db
from ..core.security import verify_token
from ..models.user import User
from ..models.project import Project, ProjectStatus, ProjectType
from ..services.ai_agent import AIAgentService
from ..services.code_generator import CodeGenerator
from ..services.deployer import DeployerService

router = APIRouter()
security = HTTPBearer()

ai_agent = AIAgentService()
code_generator = CodeGenerator()
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

@router.post("/analyze")
async def analyze_request(
    request_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze user request and provide project specification.
    """
    try:
        user_request = request_data.get("request", "")
        if not user_request:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request text is required"
            )
        
        # Use AI agent to analyze the request
        analysis = await ai_agent.analyze_request(user_request)
        
        return {
            "success": True,
            "analysis": analysis,
            "estimated_time": "2-5 minutes",
            "complexity": analysis.get("complexity", "medium")
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@router.post("/generate")
async def generate_project(
    project_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a complete full-stack application with custom framework selection.
    """
    try:
        project_name = project_data.get("name", "")
        user_request = project_data.get("request", "")
        analysis = project_data.get("analysis", {})
        tech_stack = project_data.get("tech_stack", {})
        
        if not project_name or not user_request:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project name and request are required"
            )
        
        # Check if project name already exists for user
        existing_project = db.query(Project).filter(
            Project.name == project_name,
            Project.owner_id == current_user.id
        ).first()
        
        if existing_project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project with this name already exists"
            )
        
        # Create project in database
        project = Project(
            name=project_name,
            description=analysis.get("description", ""),
            project_type=ProjectType(analysis.get("project_type", "web_app")),
            status=ProjectStatus.CREATING,
            owner_id=current_user.id,
            config=analysis.get("config", {}),
            features=analysis.get("features", []),
            integrations=analysis.get("integrations", [])
        )
        
        db.add(project)
        db.commit()
        db.refresh(project)
        
        # Generate project files using AI
        try:
            project.status = ProjectStatus.BUILDING
            db.commit()
            
            # Use AI agent to generate complete project with custom tech stack
            generated_project = await ai_agent.generate_project(analysis, project_name, tech_stack)
            
            # Save generated files to disk
            project_path = await save_project_files(project.id, generated_project["files"])
            
            # Update project with file path
            project.project_path = project_path
            project.status = ProjectStatus.ACTIVE
            db.commit()
            
            return {
                "success": True,
                "project": {
                    "id": project.id,
                    "name": project.name,
                    "type": project.project_type,
                    "status": project.status,
                    "tech_stack": generated_project.get("tech_stack", {}),
                    "created_at": project.created_at.isoformat(),
                    "project_path": project_path
                },
                "files_generated": len(generated_project["files"]),
                "message": f"🎉 {project_name} has been successfully generated!"
            }
            
        except Exception as e:
            # Update project status to error
            project.status = ProjectStatus.ERROR
            db.commit()
            raise e
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Project generation failed: {str(e)}"
        )

@router.post("/modify/{project_id}")
async def modify_project(
    project_id: int,
    modification_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Modify an existing project based on user request.
    """
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
        
        modification_request = modification_data.get("request", "")
        if not modification_request:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Modification request is required"
            )
        
        # Update project status
        project.status = ProjectStatus.BUILDING
        db.commit()
        
        # Use AI agent to modify project
        modification_result = await ai_agent.modify_project(project_id, modification_request)
        
        # Update project status
        project.status = ProjectStatus.ACTIVE
        db.commit()
        
        return {
            "success": True,
            "project_id": project_id,
            "modifications": modification_result,
            "message": "Project successfully modified!"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        # Reset project status on error
        if 'project' in locals():
            project.status = ProjectStatus.ERROR
            db.commit()
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Project modification failed: {str(e)}"
        )

@router.get("/templates")
async def get_templates(current_user: User = Depends(get_current_user)):
    """
    Get available project templates.
    """
    try:
        templates = await ai_agent.get_project_templates()
        return {
            "success": True,
            "templates": templates
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch templates: {str(e)}"
        )

@router.post("/template/{template_id}")
async def create_from_template(
    template_id: str,
    project_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a project from a template.
    """
    try:
        project_name = project_data.get("name", "")
        customizations = project_data.get("customizations", {})
        
        if not project_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project name is required"
            )
        
        # Check if project name already exists
        existing_project = db.query(Project).filter(
            Project.name == project_name,
            Project.owner_id == current_user.id
        ).first()
        
        if existing_project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project with this name already exists"
            )
        
        # Get template information
        templates = await ai_agent.get_project_templates()
        template = next((t for t in templates if t["id"] == template_id), None)
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )
        
        # Create analysis from template
        analysis = {
            "project_type": template_id,
            "features": template["features"],
            "tech_recommendations": {
                "frontend": "react",
                "backend": "fastapi",
                "database": "mysql"
            },
            "integrations": [],
            "customizations": customizations
        }
        
        # Create project
        project = Project(
            name=project_name,
            description=template["description"],
            project_type=ProjectType(template_id),
            status=ProjectStatus.CREATING,
            owner_id=current_user.id,
            config=customizations,
            features=template["features"]
        )
        
        db.add(project)
        db.commit()
        db.refresh(project)
        
        # Generate project from template
        project.status = ProjectStatus.BUILDING
        db.commit()
        
        generated_project = await ai_agent.generate_project(analysis, project_name)
        project_path = await save_project_files(project.id, generated_project["files"])
        
        project.project_path = project_path
        project.status = ProjectStatus.ACTIVE
        db.commit()
        
        return {
            "success": True,
            "project": {
                "id": project.id,
                "name": project.name,
                "type": project.project_type,
                "status": project.status,
                "template_used": template_id
            },
            "message": f"🎉 {project_name} created from {template['name']} template!"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Template creation failed: {str(e)}"
        )

@router.get("/capabilities")
async def get_capabilities():
    """
    Get AI agent capabilities and supported features.
    """
    return {
        "success": True,
        "capabilities": {
            "project_types": [
                "web_app",
                "dashboard", 
                "ecommerce",
                "blog",
                "chat",
                "crm",
                "api",
                "mobile_app"
            ],
            "frameworks": {
                "frontend": ["react", "nextjs", "vue", "angular", "react_native", "flutter"],
                "backend": ["fastapi", "express", "nestjs", "django", "spring_boot", "gin"],
                "database": ["mysql", "postgresql", "mongodb", "redis", "sqlite", "firebase"]
            },
            "features": [
                "authentication",
                "responsive_design",
                "real_time_updates",
                "file_upload",
                "email_notifications",
                "payment_processing",
                "admin_panel",
                "api_documentation",
                "user_management",
                "analytics",
                "search_functionality",
                "social_login",
                "mobile_responsive",
                "seo_optimization",
                "internationalization",
                "offline_support",
                "push_notifications"
            ],
            "integrations": [
                "stripe",
                "openai",
                "gemini",
                "google_auth",
                "email_service",
                "cloud_storage",
                "firebase",
                "aws_services",
                "social_media_apis"
            ],
            "deployment_platforms": [
                "docker",
                "vercel",
                "netlify",
                "aws",
                "gcp",
                "azure",
                "heroku",
                "railway"
            ]
        }
    }

@router.get("/frameworks")
async def get_supported_frameworks(current_user: User = Depends(get_current_user)):
    """
    Get detailed information about supported frameworks.
    """
    try:
        frameworks = await ai_agent.get_supported_frameworks()
        return {
            "success": True,
            "frameworks": frameworks
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch frameworks: {str(e)}"
        )

@router.post("/recommend-stack")
async def recommend_technology_stack(
    analysis_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """
    Get technology stack recommendations based on project analysis.
    """
    try:
        analysis = analysis_data.get("analysis", {})
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project analysis is required"
            )
        
        recommendations = await ai_agent.get_framework_recommendations(analysis)
        return {
            "success": True,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recommendations: {str(e)}"
        )

@router.post("/generate-with-stack")
async def generate_project_with_custom_stack(
    project_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate project with custom technology stack selection.
    """
    try:
        project_name = project_data.get("name", "")
        analysis = project_data.get("analysis", {})
        frontend_framework = project_data.get("frontend_framework", "react")
        backend_framework = project_data.get("backend_framework", "fastapi")
        database = project_data.get("database", "mysql")
        
        if not project_name or not analysis:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project name and analysis are required"
            )
        
        # Check if project name already exists
        existing_project = db.query(Project).filter(
            Project.name == project_name,
            Project.owner_id == current_user.id
        ).first()
        
        if existing_project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project with this name already exists"
            )
        
        # Create project in database
        project = Project(
            name=project_name,
            description=analysis.get("description", ""),
            project_type=ProjectType(analysis.get("project_type", "web_app")),
            status=ProjectStatus.CREATING,
            owner_id=current_user.id,
            config={
                "tech_stack": {
                    "frontend": frontend_framework,
                    "backend": backend_framework,
                    "database": database
                }
            },
            features=analysis.get("features", []),
            integrations=analysis.get("integrations", [])
        )
        
        db.add(project)
        db.commit()
        db.refresh(project)
        
        try:
            project.status = ProjectStatus.BUILDING
            db.commit()
            
            # Generate project with custom stack
            generated_project = await ai_agent.generate_project_with_custom_stack(
                analysis,
                project_name,
                frontend_framework,
                backend_framework,
                database
            )
            
            # Save generated files
            project_path = await save_project_files(project.id, generated_project["files"])
            
            project.project_path = project_path
            project.status = ProjectStatus.ACTIVE
            db.commit()
            
            return {
                "success": True,
                "project": {
                    "id": project.id,
                    "name": project.name,
                    "type": project.project_type,
                    "status": project.status,
                    "tech_stack": {
                        "frontend": frontend_framework,
                        "backend": backend_framework,
                        "database": database
                    },
                    "created_at": project.created_at.isoformat(),
                    "project_path": project_path
                },
                "files_generated": len(generated_project["files"]),
                "message": f"🎉 {project_name} generated with {frontend_framework} + {backend_framework} + {database}!"
            }
            
        except Exception as e:
            project.status = ProjectStatus.ERROR
            db.commit()
            raise e
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Custom stack generation failed: {str(e)}"
        )

async def save_project_files(project_id: int, files: Dict[str, str]) -> str:
    """
    Save generated project files to disk.
    """
    project_dir = Path(f"generated_projects/project_{project_id}")
    project_dir.mkdir(parents=True, exist_ok=True)
    
    for file_path, content in files.items():
        full_path = project_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return str(project_dir.absolute())