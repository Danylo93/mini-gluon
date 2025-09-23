"""
Template-related models.
"""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class TemplateInfo(BaseModel):
    """Template information model."""
    
    id: str
    name: str
    description: str
    language: str
    type: str
    tags: Optional[List[str]] = Field(default_factory=list)
    complexity: str = Field(default="beginner", description="Template complexity level")
    estimated_time: Optional[str] = Field(default=None, description="Estimated setup time")


class LanguageInfo(BaseModel):
    """Programming language information model."""
    
    id: str
    name: str
    description: str
    icon: str
    version: Optional[str] = None
    website: Optional[str] = None
    documentation: Optional[str] = None


class TemplateFile(BaseModel):
    """Template file model."""
    
    path: str
    content: str
    is_binary: bool = False
    permissions: Optional[str] = None


class Template(BaseModel):
    """Complete template model."""
    
    id: str
    name: str
    description: str
    language: str
    type: str
    files: Dict[str, str] = Field(description="Template files with content")
    variables: Optional[Dict[str, str]] = Field(default_factory=dict, description="Template variables")
    dependencies: Optional[List[str]] = Field(default_factory=list, description="Required dependencies")
    setup_instructions: Optional[str] = Field(default=None, description="Setup instructions")


class TemplateListResponse(BaseModel):
    """Response model for template list."""
    
    templates: List[TemplateInfo]
    total: int
    language: str


class LanguageListResponse(BaseModel):
    """Response model for language list."""
    
    languages: List[LanguageInfo]
    total: int
