from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import traceback

from .core.config import settings
# Import database components with error handling
try:
    from .core.database import get_db, create_tables
    DATABASE_AVAILABLE = True
except Exception as e:
    print(f"Database initialization failed: {e}")
    DATABASE_AVAILABLE = False
    # Create mock functions
    def get_db():
        class MockDB:
            def execute(self, query):
                return None
            def close(self):
                pass
        yield MockDB()
    
    def create_tables():
        print("Database not available, skipping table creation")

from .api import auth, projects, builder, deployment, realtime, ai_chat, integrations

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI Agent for building unlimited full-stack applications"
)

# Add CORS middleware using the new property
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
try:
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
    app.include_router(builder.router, prefix="/api/builder", tags=["AI Builder"])
    app.include_router(deployment.router, prefix="/api/deployment", tags=["Deployment"])
    app.include_router(realtime.router, prefix="/api/realtime", tags=["Real-time Creation"])
    app.include_router(ai_chat.router, prefix="/api/ai", tags=["AI Chat"])
    app.include_router(integrations.router, prefix="/api/integrations", tags=["Integrations"])
    print("All routers included successfully")
except Exception as e:
    print(f"Error including routers: {e}")
    print(traceback.format_exc())

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    try:
        if DATABASE_AVAILABLE:
            create_tables()
        print(f"🚀 {settings.APP_NAME} v{settings.VERSION} started successfully!")
        print(f"📖 API Documentation: http://localhost:8000/docs")
        print(f"🌐 CORS Origins: {settings.CORS_ORIGINS_LIST}")
    except Exception as e:
        print(f"Startup error: {e}")
        print(traceback.format_exc())
        print("Application will start with limited functionality")

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
async def health_check(db: None = None):
    """Health check endpoint."""
    # Only check database if it's available
    if DATABASE_AVAILABLE:
        try:
            # Test database connection
            from .core.database import get_db
            from sqlalchemy import text
            db_gen = get_db()
            db = next(db_gen)
            db.execute(text("SELECT 1"))
            db_gen.close()
            database_status = "connected"
        except Exception as e:
            database_status = f"connection failed: {str(e)}"
    else:
        database_status = "not available"
    
    return {
        "status": "healthy",
        "database": database_status,
        "timestamp": "2024-01-01T00:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )