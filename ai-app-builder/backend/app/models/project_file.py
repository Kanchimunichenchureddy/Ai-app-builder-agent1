from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class ProjectFile(Base):
    __tablename__ = "project_files"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_content = Column(Text, nullable=True)
    file_type = Column(String(50), nullable=True)
    file_size = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="files")
    
    # Indexes
    __table_args__ = (
        Index('idx_project_files_project_id', 'project_id'),
        Index('idx_project_files_path', 'file_path'),
        Index('idx_project_files_type', 'file_type'),
    )