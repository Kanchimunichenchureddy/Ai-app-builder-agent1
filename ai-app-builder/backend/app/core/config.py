import os
from pydantic_settings import BaseSettings
from typing import Optional, List
from pydantic import Field

class Settings(BaseSettings):
    # App Configuration
    APP_NAME: str = "AI App Builder Agent"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database Environment Variables (from .env)
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "tejadot12345")
    DB_NAME: str = os.getenv("DB_NAME", "appforge")
    
    # Database - Construct URL with proper error handling
    @property
    def DATABASE_URL(self) -> str:
        # Check if DATABASE_URL is directly provided in environment
        direct_url = os.getenv("DATABASE_URL")
        if direct_url:
            return direct_url
            
        # Construct URL from individual components
        try:
            # Check if we have MySQL driver available
            import pymysql
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        except ImportError:
            # Fallback to SQLite
            return "sqlite:///./app.db"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # AI Services - Only OpenRouter now
    OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    
    # External APIs
    STRIPE_SECRET_KEY: Optional[str] = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_PUBLISHABLE_KEY: Optional[str] = os.getenv("STRIPE_PUBLISHABLE_KEY")
    STRIPE_WEBHOOK_SECRET: Optional[str] = os.getenv("STRIPE_WEBHOOK_SECRET")
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: Optional[str] = os.getenv("GOOGLE_REDIRECT_URI")
    
    # File Storage
    PROJECTS_DIR: str = os.getenv("PROJECTS_DIR", "generated_projects")
    TEMPLATES_DIR: str = os.getenv("TEMPLATES_DIR", "templates")
    
    # Docker
    DOCKER_REGISTRY: Optional[str] = os.getenv("DOCKER_REGISTRY")
    
    # CORS - Directly use the CORS_ORIGINS environment variable
    # Use Field to prevent Pydantic from automatically parsing it as JSON
    CORS_ORIGINS: str = Field(
        default=os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001"),
        description="Comma-separated list of allowed CORS origins"
    )
    
    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        """Parse CORS origins from string to list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    class Config:
        env_file = ".env"
        # Prevent Pydantic from automatically creating fields for environment variables
        extra = "ignore"

# Create settings instance
settings = Settings()