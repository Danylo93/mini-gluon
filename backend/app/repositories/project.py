"""
Project repository for database operations.
"""
from typing import List, Optional
from datetime import datetime

from app.models.project import Project
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository):
    """Repository for project operations."""
    
    def __init__(self):
        super().__init__("projects", Project)
    
    async def get_by_name(self, name: str) -> Optional[Project]:
        """Get project by name."""
        return await self.get_by_field("name", name)
    
    async def get_by_github_username(self, username: str) -> List[Project]:
        """Get projects by GitHub username."""
        return await self.get_all(filter_dict={"github_username": username})
    
    async def get_by_language(self, language: str) -> List[Project]:
        """Get projects by programming language."""
        return await self.get_all(filter_dict={"language": language})
    
    async def get_recent_projects(self, limit: int = 10) -> List[Project]:
        """Get recently created projects."""
        return await self.get_all(limit=limit)
    
    async def update_status(self, project_id: str, status: str) -> Optional[Project]:
        """Update project status."""
        return await self.update(project_id, {"status": status})
    
    async def get_project_stats(self) -> dict:
        """Get project statistics."""
        total_projects = await self.count()
        languages = await self.collection.distinct("language")
        
        stats = {
            "total_projects": total_projects,
            "languages": len(languages),
            "language_breakdown": {}
        }
        
        for language in languages:
            count = await self.count({"language": language})
            stats["language_breakdown"][language] = count
        
        return stats
