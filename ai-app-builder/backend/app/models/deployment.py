from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum

class DeploymentStatus(str, enum.Enum):
    PENDING = "pending"
    BUILDING = "building"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    FAILED = "failed"
    STOPPED = "stopped"

class DeploymentPlatform(str, enum.Enum):
    DOCKER = "docker"
    VERCEL = "vercel"
    NETLIFY = "netlify"
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    HEROKU = "heroku"
    DIGITAL_OCEAN = "digital_ocean"

class Deployment(Base):
    __tablename__ = "deployments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    platform = Column(Enum(DeploymentPlatform), nullable=False)
    status = Column(Enum(DeploymentStatus), default=DeploymentStatus.PENDING)
    
    # Deployment URLs
    url = Column(String(500), nullable=True)
    api_url = Column(String(500), nullable=True)
    admin_url = Column(String(500), nullable=True)
    
    # Configuration
    config = Column(JSON, nullable=True)  # Platform-specific config
    environment_variables = Column(JSON, nullable=True)
    
    # Build Information
    build_logs = Column(Text, nullable=True)
    deployment_logs = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Metadata
    deployed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships - using string references to avoid circular imports
    project = relationship("Project", back_populates="deployments")
    user = relationship("User", back_populates="deployments")