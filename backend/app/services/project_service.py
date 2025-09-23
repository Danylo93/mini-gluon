"""
Project service for managing project operations.
"""
from typing import Dict, List, Optional
import logging
from datetime import datetime

from app.core.exceptions import ValidationError, GitHubError, DatabaseError
from app.core.logging import get_logger
from app.models.project import Project, ProjectRequest, ProjectResponse
from app.repositories.project import ProjectRepository
from app.services.github_service import GitHubService
from app.services.template_service import TemplateService

logger = get_logger(__name__)


class ProjectService:
    """Service for project operations."""
    
    def __init__(
        self,
        project_repository: ProjectRepository,
        github_service: GitHubService,
        template_service: TemplateService
    ):
        self.project_repository = project_repository
        self.github_service = github_service
        self.template_service = template_service
    
    async def create_project(self, request: ProjectRequest) -> ProjectResponse:
        """
        Create a new project with GitHub repository.
        
        Args:
            request: Project creation request
            
        Returns:
            Project creation response
        """
        try:
            logger.info(f"Creating project: {request.name}")
            
            # Validate template exists
            template = self.template_service.get_template(request.language, request.template_id)
            
            # Prepare template variables
            template_variables = {
                "project_name": request.name,
                "project_description": request.description
            }
            
            # Validate template variables
            self.template_service.validate_template_variables(template, template_variables)
            
            # Process template files
            processed_files = self.template_service.process_template(template, template_variables)
            
            # Create GitHub repository
            repo_info = await self.github_service.create_repository(
                name=request.name,
                description=request.description,
                private=False
            )
            
            # Create files in repository
            await self.github_service.create_files(
                repo_name=repo_info["name"],
                files=processed_files,
                commit_message=f"Initial commit: {request.name}"
            )
            
            # Save project to database
            project = Project(
                name=request.name,
                description=request.description,
                language=request.language,
                template_id=request.template_id,
                github_username=request.github_username,
                repository_url=repo_info["html_url"],
                status="created",
                metadata={
                    "template_used": template.id,
                    "files_created": len(processed_files),
                    "github_repo": repo_info["name"]
                }
            )
            
            created_project = await self.project_repository.create(project)
            
            logger.info(f"Successfully created project: {request.name}")
            
            return ProjectResponse(
                success=True,
                message=f"Project '{request.name}' created successfully!",
                repository_url=repo_info["html_url"],
                project_id=created_project.id
            )
            
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
        except GitHubError as e:
            logger.error(f"GitHub error: {str(e)}")
            raise
        except DatabaseError as e:
            logger.error(f"Database error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating project: {str(e)}")
            raise ValidationError(f"Failed to create project: {str(e)}")
    
    async def get_projects(
        self, 
        skip: int = 0, 
        limit: int = 50,
        language: Optional[str] = None,
        github_username: Optional[str] = None
    ) -> List[Project]:
        """
        Get projects with optional filtering.
        
        Args:
            skip: Number of projects to skip
            limit: Maximum number of projects to return
            language: Filter by programming language
            github_username: Filter by GitHub username
            
        Returns:
            List of projects
        """
        try:
            filter_dict = {}
            if language:
                filter_dict["language"] = language
            if github_username:
                filter_dict["github_username"] = github_username
            
            projects = await self.project_repository.get_all(
                skip=skip,
                limit=limit,
                filter_dict=filter_dict
            )
            
            return projects
            
        except Exception as e:
            logger.error(f"Error getting projects: {str(e)}")
            raise DatabaseError(f"Failed to get projects: {str(e)}")
    
    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Get project by ID."""
        try:
            return await self.project_repository.get_by_id(project_id)
        except Exception as e:
            logger.error(f"Error getting project {project_id}: {str(e)}")
            raise DatabaseError(f"Failed to get project: {str(e)}")
    
    async def get_project_by_name(self, name: str) -> Optional[Project]:
        """Get project by name."""
        try:
            return await self.project_repository.get_by_name(name)
        except Exception as e:
            logger.error(f"Error getting project {name}: {str(e)}")
            raise DatabaseError(f"Failed to get project: {str(e)}")
    
    async def get_recent_projects(self, limit: int = 10) -> List[Project]:
        """Get recently created projects."""
        try:
            return await self.project_repository.get_recent_projects(limit)
        except Exception as e:
            logger.error(f"Error getting recent projects: {str(e)}")
            raise DatabaseError(f"Failed to get recent projects: {str(e)}")
    
    async def update_project_status(self, project_id: str, status: str) -> Optional[Project]:
        """Update project status."""
        try:
            valid_statuses = ["created", "building", "ready", "failed", "deleted"]
            if status not in valid_statuses:
                raise ValidationError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            
            return await self.project_repository.update_status(project_id, status)
        except Exception as e:
            logger.error(f"Error updating project status: {str(e)}")
            raise DatabaseError(f"Failed to update project status: {str(e)}")
    
    async def get_project_statistics(self) -> Dict:
        """Get project statistics."""
        try:
            return await self.project_repository.get_project_stats()
        except Exception as e:
            logger.error(f"Error getting project statistics: {str(e)}")
            raise DatabaseError(f"Failed to get project statistics: {str(e)}")
    
    async def delete_project(self, project_id: str) -> bool:
        """Delete a project and its GitHub repository."""
        try:
            project = await self.project_repository.get_by_id(project_id)
            if not project:
                raise ValidationError("Project not found")
            
            # Extract repository name from URL
            repo_name = project.metadata.get("github_repo")
            if repo_name:
                await self.github_service.delete_repository(repo_name)
            
            # Delete from database
            success = await self.project_repository.delete(project_id)
            
            if success:
                logger.info(f"Successfully deleted project: {project.name}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error deleting project: {str(e)}")
            raise DatabaseError(f"Failed to delete project: {str(e)}")
