"""
Status and health check API endpoints.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
import logging

from app.core.logging import get_logger
from app.core.exceptions import DatabaseError
from app.models.status import StatusCheck, StatusCheckCreate, HealthCheck
from app.repositories.status import StatusCheckRepository
from app.services.github_service import GitHubService
from app.core.database import database

logger = get_logger(__name__)

# Create router
router = APIRouter(prefix="/status", tags=["status"])

# Track application start time for uptime calculation
app_start_time = datetime.utcnow()


def get_status_repository() -> StatusCheckRepository:
    """Dependency to get status check repository instance."""
    return StatusCheckRepository()


def get_github_service() -> GitHubService:
    """Dependency to get GitHub service instance."""
    return GitHubService()


@router.get("/health", response_model=HealthCheck)
async def health_check(
    github_service: GitHubService = Depends(get_github_service)
):
    """
    Health check endpoint.
    
    Returns the health status of the application and its dependencies.
    """
    try:
        # Calculate uptime
        uptime = (datetime.utcnow() - app_start_time).total_seconds()
        
        # Check database connection
        try:
            db = database.get_database()
            await db.command("ping")
            db_status = "connected"
        except Exception:
            db_status = "disconnected"
        
        # Check GitHub API connection
        try:
            github_connected = await github_service.test_connection()
            github_status = "connected" if github_connected else "disconnected"
        except Exception:
            github_status = "disconnected"
        
        return HealthCheck(
            status="healthy" if db_status == "connected" and github_status == "connected" else "unhealthy",
            version="1.0.0",
            uptime=uptime,
            services={
                "database": db_status,
                "github_api": github_status
            },
            database=db_status,
            github_api=github_status
        )
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")


@router.post("/check", response_model=StatusCheck, status_code=201)
async def create_status_check(
    request: StatusCheckCreate,
    status_repository: StatusCheckRepository = Depends(get_status_repository)
):
    """
    Create a new status check record.
    
    - **client_name**: Name of the client making the check
    - **metadata**: Additional metadata (optional)
    """
    try:
        status_check = StatusCheck(
            client_name=request.client_name,
            metadata=request.metadata
        )
        
        created_check = await status_repository.create(status_check)
        logger.info(f"Status check created for client: {request.client_name}")
        
        return created_check
    except Exception as e:
        logger.error(f"Error creating status check: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create status check")


@router.get("/checks", response_model=List[StatusCheck])
async def get_status_checks(
    limit: int = 100,
    status_repository: StatusCheckRepository = Depends(get_status_repository)
):
    """
    Get recent status checks.
    
    - **limit**: Maximum number of status checks to return (default: 100)
    """
    try:
        checks = await status_repository.get_recent_checks(limit)
        return checks
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting status checks: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/checks/client/{client_name}", response_model=List[StatusCheck])
async def get_status_checks_by_client(
    client_name: str,
    status_repository: StatusCheckRepository = Depends(get_status_repository)
):
    """
    Get status checks for a specific client.
    
    - **client_name**: Name of the client
    """
    try:
        checks = await status_repository.get_by_client(client_name)
        return checks
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting status checks for client {client_name}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stats/clients")
async def get_client_statistics(
    status_repository: StatusCheckRepository = Depends(get_status_repository)
):
    """
    Get statistics about client status checks.
    
    Returns information about clients and their check frequency.
    """
    try:
        stats = await status_repository.get_client_stats()
        return stats
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting client statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/cleanup")
async def cleanup_old_status_checks(
    days: int = 30,
    status_repository: StatusCheckRepository = Depends(get_status_repository)
):
    """
    Clean up old status checks.
    
    - **days**: Number of days to keep status checks (default: 30)
    
    Removes status checks older than the specified number of days.
    """
    try:
        deleted_count = await status_repository.cleanup_old_checks(days)
        logger.info(f"Cleaned up {deleted_count} old status checks")
        
        return {
            "message": f"Cleaned up {deleted_count} status checks older than {days} days",
            "deleted_count": deleted_count
        }
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error cleaning up status checks: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
