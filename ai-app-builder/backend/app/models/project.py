from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum

class ProjectType(str, enum.Enum):
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    API = "api"
    DASHBOARD = "dashboard"
    ECOMMERCE = "ecommerce"
    BLOG = "blog"
    CRM = "crm"
    CHAT = "chat"
    CUSTOM = "custom"

class ProjectStatus(str, enum.Enum):
    CREATING = "creating"
    ACTIVE = "active"
    BUILDING = "building"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    ERROR = "error"
    ARCHIVED = "archived"

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    project_type = Column(Enum(ProjectType), nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.CREATING)
    
    # Technical Configuration
    frontend_framework = Column(String(100), default="react")
    backend_framework = Column(String(100), default="fastapi")
    database_type = Column(String(100), default="mysql")
    
    # Project Configuration
    config = Column(JSON, nullable=True)  # Store project-specific config
    features = Column(JSON, nullable=True)  # Store enabled features
    integrations = Column(JSON, nullable=True)  # Store API integrations
    
    # File Paths
    project_path = Column(String(500), nullable=True)
    repository_url = Column(String(500), nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships - using string references to avoid circular imports
    owner = relationship("User", back_populates="projects")
    deployments = relationship("Deployment", back_populates="project", cascade="all, delete-orphan")
    files = relationship("ProjectFile", back_populates="project", cascade="all, delete-orphan")