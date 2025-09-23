"""
Status and health check models.
"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from app.models.base import BaseDocument


class StatusCheckCreate(BaseModel):
    """Request model for creating a status check."""
    
    client_name: str = Field(..., min_length=1, max_length=100, description="Client name")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class StatusCheck(BaseDocument):
    """Status check document model."""
    
    client_name: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class HealthCheck(BaseModel):
    """Health check response model."""
    
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str
    uptime: Optional[float] = None
    services: Dict[str, str] = Field(default_factory=dict, description="Service statuses")
    database: str = "connected"
    github_api: str = "connected"
