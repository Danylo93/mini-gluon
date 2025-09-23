"""
Validation utilities and helpers.
"""
import re
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse


def validate_project_name(name: str) -> bool:
    """
    Validate project name format.
    
    Args:
        name: Project name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not name or len(name) < 1 or len(name) > 100:
        return False
    
    # Allow alphanumeric, hyphens, underscores, and spaces
    pattern = r'^[a-zA-Z0-9\s\-_]+$'
    return bool(re.match(pattern, name))


def validate_github_username(username: str) -> bool:
    """
    Validate GitHub username format.
    
    Args:
        username: GitHub username to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not username or len(username) < 1 or len(username) > 39:
        return False
    
    # GitHub usernames can contain alphanumeric and hyphens, but not start/end with hyphen
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?$'
    return bool(re.match(pattern, username))


def validate_repository_name(name: str) -> bool:
    """
    Validate repository name format.
    
    Args:
        name: Repository name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not name or len(name) < 1 or len(name) > 100:
        return False
    
    # Repository names can contain alphanumeric, hyphens, underscores, and dots
    pattern = r'^[a-zA-Z0-9\-_.]+$'
    return bool(re.match(pattern, name))


def validate_url(url: str) -> bool:
    """
    Validate URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file system usage.
    
    Args:
        filename: Filename to sanitize
        
    Returns:
        Sanitized filename
    """
    # Remove or replace dangerous characters
    dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
    sanitized = filename
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    
    # Ensure it's not empty
    if not sanitized:
        sanitized = 'unnamed'
    
    return sanitized


def validate_template_variables(
    template_variables: Dict[str, str], 
    provided_variables: Dict[str, Any]
) -> List[str]:
    """
    Validate template variables.
    
    Args:
        template_variables: Required template variables
        provided_variables: Variables provided by user
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Check for missing required variables
    required_vars = set(template_variables.keys())
    provided_vars = set(provided_variables.keys())
    missing_vars = required_vars - provided_vars
    
    if missing_vars:
        errors.append(f"Missing required variables: {', '.join(missing_vars)}")
    
    # Check for extra variables
    extra_vars = provided_vars - required_vars
    if extra_vars:
        errors.append(f"Unknown variables: {', '.join(extra_vars)}")
    
    # Validate variable values
    for var_name, var_value in provided_variables.items():
        if var_name in template_variables:
            if not isinstance(var_value, str):
                errors.append(f"Variable '{var_name}' must be a string")
            elif len(var_value) == 0:
                errors.append(f"Variable '{var_name}' cannot be empty")
            elif len(var_value) > 1000:
                errors.append(f"Variable '{var_name}' is too long (max 1000 characters)")
    
    return errors


def validate_pagination_params(skip: int, limit: int) -> List[str]:
    """
    Validate pagination parameters.
    
    Args:
        skip: Number of items to skip
        limit: Maximum number of items to return
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    if skip < 0:
        errors.append("Skip parameter must be non-negative")
    
    if limit < 1:
        errors.append("Limit parameter must be at least 1")
    
    if limit > 1000:
        errors.append("Limit parameter cannot exceed 1000")
    
    return errors
