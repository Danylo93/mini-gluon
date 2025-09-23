"""
Project-related models.
"""
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

from app.models.base import BaseDocument


class ProjectRequest(BaseModel):
    """Request model for creating a new project."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    description: str = Field(..., min_length=1, max_length=500, description="Project description")
    language: str = Field(..., description="Programming language")
    template_id: str = Field(..., description="Template identifier")
    github_username: str = Field(..., description="GitHub username")
    
    @validator('name')
    def validate_name(cls, v):
        """Validate project name format."""
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Project name must contain only alphanumeric characters, hyphens, and underscores')
        return v.lower().replace(' ', '-')
    
    @validator('language')
    def validate_language(cls, v):
        """Validate supported language."""
        supported_languages = ['java', 'dotnet', 'python', 'javascript', 'typescript']
        if v.lower() not in supported_languages:
            raise ValueError(f'Language must be one of: {", ".join(supported_languages)}')
        return v.lower()


class ProjectResponse(BaseModel):
    """Response model for project creation."""
    
    success: bool = True
    message: str
    repository_url: Optional[str] = None
    project_id: Optional[str] = None


class Project(BaseDocument):
    """Project document model."""
    
    name: str
    description: str
    language: str
    template_id: str
    github_username: str
    repository_url: str
    status: str = Field(default="created", description="Project status")
    metadata: Optional[dict] = Field(default_factory=dict, description="Additional metadata")


class ProjectListResponse(BaseModel):
    """Response model for project list."""
    
    projects: list[Project]
    total: int
    page: int = 1
    page_size: int = 50
