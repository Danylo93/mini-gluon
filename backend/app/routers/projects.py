"""
Project-related API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
import logging

from app.core.logging import get_logger
from app.core.exceptions import ValidationError, NotFoundError, DatabaseError
from app.models.project import Project, ProjectRequest, ProjectResponse, ProjectListResponse
from app.services.project_service import ProjectService
from app.services.github_service import GitHubService
from app.services.template_service import TemplateService
from app.repositories.project import ProjectRepository

logger = get_logger(__name__)

# Create router
router = APIRouter(prefix="/projects", tags=["projects"])


def get_project_service() -> ProjectService:
    """Dependency to get project service instance."""
    project_repo = ProjectRepository()
    github_service = GitHubService()
    template_service = TemplateService()
    return ProjectService(project_repo, github_service, template_service)


@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    request: ProjectRequest,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Create a new project with GitHub repository.
    
    - **name**: Project name (will be used as repository name)
    - **description**: Project description
    - **language**: Programming language (java, dotnet, etc.)
    - **template_id**: Template identifier
    - **github_username**: GitHub username for the repository
    """
    try:
        return await project_service.create_project(request)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=ProjectListResponse)
async def get_projects(
    skip: int = Query(0, ge=0, description="Number of projects to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of projects to return"),
    language: Optional[str] = Query(None, description="Filter by programming language"),
    github_username: Optional[str] = Query(None, description="Filter by GitHub username"),
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Get projects with optional filtering and pagination.
    
    - **skip**: Number of projects to skip (for pagination)
    - **limit**: Maximum number of projects to return (1-100)
    - **language**: Filter by programming language
    - **github_username**: Filter by GitHub username
    """
    try:
        projects = await project_service.get_projects(
            skip=skip,
            limit=limit,
            language=language,
            github_username=github_username
        )
        
        total = await project_service.project_repository.count()
        
        return ProjectListResponse(
            projects=projects,
            total=total,
            page=(skip // limit) + 1,
            page_size=limit
        )
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting projects: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id: str,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Get a specific project by ID.
    
    - **project_id**: Project identifier
    """
    try:
        project = await project_service.get_project_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/name/{project_name}", response_model=Project)
async def get_project_by_name(
    project_name: str,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Get a specific project by name.
    
    - **project_name**: Project name
    """
    try:
        project = await project_service.get_project_by_name(project_name)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting project {project_name}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/recent/", response_model=List[Project])
async def get_recent_projects(
    limit: int = Query(10, ge=1, le=50, description="Maximum number of recent projects"),
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Get recently created projects.
    
    - **limit**: Maximum number of projects to return (1-50)
    """
    try:
        return await project_service.get_recent_projects(limit)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting recent projects: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/{project_id}/status")
async def update_project_status(
    project_id: str,
    status: str,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Update project status.
    
    - **project_id**: Project identifier
    - **status**: New status (created, building, ready, failed, deleted)
    """
    try:
        project = await project_service.update_project_status(project_id, status)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"message": f"Project status updated to {status}", "project": project}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating project status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stats/overview")
async def get_project_statistics(
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Get project statistics and overview.
    """
    try:
        return await project_service.get_project_statistics()
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting project statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Delete a project and its GitHub repository.
    
    - **project_id**: Project identifier
    """
    try:
        success = await project_service.delete_project(project_id)
        if not success:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"message": "Project deleted successfully"}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
