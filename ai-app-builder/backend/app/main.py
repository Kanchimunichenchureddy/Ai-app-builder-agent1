from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from .core.config import settings
from .core.database import get_db, create_tables
from .api import auth, projects, builder, deployment, realtime, ai_chat, integrations

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI Agent for building unlimited full-stack applications"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(builder.router, prefix="/api/builder", tags=["AI Builder"])
app.include_router(deployment.router, prefix="/api/deployment", tags=["Deployment"])
app.include_router(realtime.router, prefix="/api/realtime", tags=["Real-time Creation"])
app.include_router(ai_chat.router, prefix="/api/ai", tags=["AI Chat"])
app.include_router(integrations.router, prefix="/api/integrations", tags=["Integrations"])


@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    create_tables()
    print(f"🚀 {settings.APP_NAME} v{settings.VERSION} started successfully!")
    print(f"📖 API Documentation: http://localhost:8000/docs")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.VERSION,
        "description": "AI Agent for building unlimited full-stack applications",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint."""
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )