"""
Template-related API endpoints.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends
import logging

from app.core.logging import get_logger
from app.core.exceptions import ValidationError
from app.models.template import LanguageListResponse, TemplateListResponse
from app.services.template_service import TemplateService

logger = get_logger(__name__)

# Create router
router = APIRouter(prefix="/templates", tags=["templates"])


def get_template_service() -> TemplateService:
    """Dependency to get template service instance."""
    return TemplateService()


@router.get("/languages", response_model=LanguageListResponse)
async def get_languages(
    template_service: TemplateService = Depends(get_template_service)
):
    """
    Get all supported programming languages.
    
    Returns a list of supported programming languages with their details.
    """
    try:
        languages = template_service.get_languages()
        return LanguageListResponse(
            languages=languages,
            total=len(languages)
        )
    except Exception as e:
        logger.error(f"Error getting languages: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{language}", response_model=TemplateListResponse)
async def get_templates_by_language(
    language: str,
    template_service: TemplateService = Depends(get_template_service)
):
    """
    Get available templates for a specific language.
    
    - **language**: Programming language (java, dotnet, etc.)
    
    Returns a list of available templates for the specified language.
    """
    try:
        templates = template_service.get_templates_by_language(language)
        return TemplateListResponse(
            templates=templates,
            total=len(templates),
            language=language
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting templates for language {language}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{language}/{template_id}")
async def get_template_details(
    language: str,
    template_id: str,
    template_service: TemplateService = Depends(get_template_service)
):
    """
    Get detailed information about a specific template.
    
    - **language**: Programming language
    - **template_id**: Template identifier
    
    Returns detailed information about the template including files, variables, and dependencies.
    """
    try:
        template = template_service.get_template(language, template_id)
        return {
            "template": template,
            "variables": template.variables,
            "dependencies": template.dependencies,
            "setup_instructions": template.setup_instructions,
            "file_count": len(template.files)
        }
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting template {template_id} for language {language}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{language}/{template_id}/preview")
async def preview_template(
    language: str,
    template_id: str,
    project_name: str = "my-project",
    project_description: str = "A sample project",
    template_service: TemplateService = Depends(get_template_service)
):
    """
    Preview a template with sample variables.
    
    - **language**: Programming language
    - **template_id**: Template identifier
    - **project_name**: Sample project name
    - **project_description**: Sample project description
    
    Returns a preview of the template files with variables substituted.
    """
    try:
        template = template_service.get_template(language, template_id)
        
        # Prepare sample variables
        variables = {
            "project_name": project_name,
            "project_description": project_description
        }
        
        # Validate variables
        template_service.validate_template_variables(template, variables)
        
        # Process template
        processed_files = template_service.process_template(template, variables)
        
        # Return preview (limit file content for response size)
        preview_files = {}
        for file_path, content in processed_files.items():
            # Truncate large files for preview
            if len(content) > 1000:
                content = content[:1000] + "\n... (truncated for preview)"
            preview_files[file_path] = content
        
        return {
            "template_id": template.id,
            "template_name": template.name,
            "language": template.language,
            "files": preview_files,
            "total_files": len(processed_files),
            "variables_used": variables
        }
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error previewing template {template_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
