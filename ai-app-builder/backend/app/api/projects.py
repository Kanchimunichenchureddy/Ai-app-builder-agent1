from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from ..core.database import get_db
from ..core.security import verify_token
from ..models.user import User
from ..models.project import Project, ProjectStatus, ProjectType

router = APIRouter()
security = HTTPBearer()

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

@router.get("/")
async def get_projects(
    skip: int = 0,
    limit: int = 20,
    status_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's projects with optional filtering."""
    query = db.query(Project).filter(Project.owner_id == current_user.id)
    
    # Apply filters
    if status_filter:
        try:
            status_enum = ProjectStatus(status_filter)
            query = query.filter(Project.status == status_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status filter: {status_filter}"
            )
    
    if type_filter:
        try:
            type_enum = ProjectType(type_filter)
            query = query.filter(Project.project_type == type_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid type filter: {type_filter}"
            )
    
    # Get total count
    total = query.count()
    
    # Apply pagination and ordering
    projects = query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "projects": [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "type": project.project_type,
                "status": project.status,
                "features": project.features,
                "frontend_framework": project.frontend_framework,
                "backend_framework": project.backend_framework,
                "database_type": project.database_type,
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat() if project.updated_at else None,
                "repository_url": project.repository_url
            }
            for project in projects
        ],
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/{project_id}")
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific project details."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return {
        "success": True,
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "type": project.project_type,
            "status": project.status,
            "config": project.config,
            "features": project.features,
            "integrations": project.integrations,
            "frontend_framework": project.frontend_framework,
            "backend_framework": project.backend_framework,
            "database_type": project.database_type,
            "project_path": project.project_path,
            "repository_url": project.repository_url,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat() if project.updated_at else None
        }
    }

@router.put("/{project_id}")
async def update_project(
    project_id: int,
    update_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update project information."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Update allowed fields
    allowed_fields = ["name", "description", "config", "repository_url"]
    for field, value in update_data.items():
        if field in allowed_fields and hasattr(project, field):
            setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return {
        "success": True,
        "message": "Project updated successfully",
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "updated_at": project.updated_at.isoformat()
        }
    }

@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a project."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # TODO: Clean up project files and deployments
    # if project.project_path and os.path.exists(project.project_path):
    #     shutil.rmtree(project.project_path)
    
    db.delete(project)
    db.commit()
    
    return {
        "success": True,
        "message": "Project deleted successfully"
    }

@router.get("/{project_id}/files")
async def get_project_files(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get project file structure."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if not project.project_path:
        return {
            "success": True,
            "files": {},
            "message": "No files generated yet"
        }
    
    # TODO: Implement file tree reading
    return {
        "success": True,
        "files": {},
        "message": "File listing not implemented yet"
    }

@router.get("/stats/overview")
async def get_project_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's project statistics."""
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    
    stats = {
        "total_projects": len(projects),
        "active_projects": len([p for p in projects if p.status == ProjectStatus.ACTIVE]),
        "deployed_projects": len([p for p in projects if p.status == ProjectStatus.DEPLOYED]),
        "by_type": {},
        "by_status": {},
        "recent_activity": []
    }
    
    # Count by type
    for project_type in ProjectType:
        count = len([p for p in projects if p.project_type == project_type])
        if count > 0:
            stats["by_type"][project_type.value] = count
    
    # Count by status
    for project_status in ProjectStatus:
        count = len([p for p in projects if p.status == project_status])
        if count > 0:
            stats["by_status"][project_status.value] = count
    
    # Recent activity (last 5 projects)
    recent_projects = sorted(projects, key=lambda x: x.created_at, reverse=True)[:5]
    stats["recent_activity"] = [
        {
            "id": p.id,
            "name": p.name,
            "type": p.project_type,
            "status": p.status,
            "created_at": p.created_at.isoformat()
        }
        for p in recent_projects
    ]
    
    return {
        "success": True,
        "stats": stats
    }