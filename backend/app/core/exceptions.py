"""
Custom exceptions for the application.
"""
from typing import Any, Dict, Optional


class ScaffoldForgeException(Exception):
    """Base exception for Scaffold Forge application."""
    
    def __init__(
        self, 
        message: str, 
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500
    ):
        self.message = message
        self.details = details or {}
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(ScaffoldForgeException):
    """Validation error exception."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=400)


class NotFoundError(ScaffoldForgeException):
    """Resource not found exception."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=404)


class GitHubError(ScaffoldForgeException):
    """GitHub API error exception."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=502)


class TemplateError(ScaffoldForgeException):
    """Template processing error exception."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=422)


class DatabaseError(ScaffoldForgeException):
    """Database operation error exception."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=500)
