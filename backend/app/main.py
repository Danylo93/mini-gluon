"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import logging
import time

from app.config.settings import settings
from app.core.database import database
from app.core.logging import setup_logging, get_logger
from app.core.exceptions import ScaffoldForgeException
from app.routers import projects, templates, status

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.app_version,
    debug=settings.debug,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for security
if not settings.debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"]
    )


# Global exception handler
@app.exception_handler(ScaffoldForgeException)
async def scaffold_forge_exception_handler(request: Request, exc: ScaffoldForgeException):
    """Handle custom application exceptions."""
    logger.error(f"ScaffoldForgeException: {exc.message}", extra={"details": exc.details})
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "details": exc.details
        }
    )


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Include routers
app.include_router(projects.router, prefix=settings.api_prefix)
app.include_router(templates.router, prefix=settings.api_prefix)
app.include_router(status.router, prefix=settings.api_prefix)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Scaffold Forge - Template Generator System",
        "version": settings.app_version,
        "docs_url": "/docs" if settings.debug else "Documentation not available in production",
        "health_check": "/api/status/health"
    }


# Workflow dashboard endpoint
@app.get("/workflow-dashboard")
async def workflow_dashboard():
    """Serve the workflow dashboard."""
    try:
        # Path relative to the project root
        dashboard_path = Path(__file__).parent.parent.parent / "workflow-dashboard.html"
        if dashboard_path.exists():
            with open(dashboard_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            return HTMLResponse(content=html_content)
        else:
            return HTMLResponse(
                content="<h1>Dashboard not found</h1>", 
                status_code=404
            )
    except Exception as e:
        logger.error(f"Error serving workflow dashboard: {str(e)}")
        return HTMLResponse(
            content="<h1>Error loading dashboard</h1>", 
            status_code=500
        )


# Serve static files (React app)
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    # Mount the nested static directory where React build files are located
    nested_static_dir = static_dir / "static"
    if nested_static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(nested_static_dir)), name="static")
    else:
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    # Serve React app for all non-API routes
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        """Serve React app for all non-API routes."""
        # Don't serve React app for API routes
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not found")
        
        # Serve index.html for all other routes (React Router)
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        else:
            raise HTTPException(status_code=404, detail="Frontend not built")


# Application startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Starting Scaffold Forge application...")
    
    try:
        # Connect to database
        await database.connect()
        logger.info("Database connection established")
        
        # Test GitHub connection
        from app.services.github_service import GitHubService
        github_service = GitHubService()
        github_connected = await github_service.test_connection()
        if github_connected:
            logger.info("GitHub API connection verified")
        else:
            logger.warning("GitHub API connection failed")
        
        logger.info("Application startup completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise


# Application shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down Scaffold Forge application...")
    
    try:
        # Disconnect from database
        await database.disconnect()
        logger.info("Database connection closed")
        
        logger.info("Application shutdown completed")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
