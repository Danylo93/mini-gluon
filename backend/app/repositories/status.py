"""
Status check repository for database operations.
"""
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.status import StatusCheck
from app.repositories.base import BaseRepository


class StatusCheckRepository(BaseRepository):
    """Repository for status check operations."""
    
    def __init__(self):
        super().__init__("status_checks", StatusCheck)
    
    async def get_recent_checks(self, limit: int = 100) -> List[StatusCheck]:
        """Get recent status checks."""
        return await self.get_all(limit=limit)
    
    async def get_by_client(self, client_name: str) -> List[StatusCheck]:
        """Get status checks by client name."""
        return await self.get_all(filter_dict={"client_name": client_name})
    
    async def get_checks_since(self, since: datetime) -> List[StatusCheck]:
        """Get status checks since a specific time."""
        return await self.get_all(filter_dict={"created_at": {"$gte": since}})
    
    async def cleanup_old_checks(self, days: int = 30) -> int:
        """Remove status checks older than specified days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = await self.collection.delete_many({
            "created_at": {"$lt": cutoff_date}
        })
        return result.deleted_count
    
    async def get_client_stats(self) -> dict:
        """Get statistics about client status checks."""
        pipeline = [
            {
                "$group": {
                    "_id": "$client_name",
                    "count": {"$sum": 1},
                    "last_check": {"$max": "$created_at"}
                }
            },
            {
                "$sort": {"count": -1}
            }
        ]
        
        stats = []
        async for result in self.collection.aggregate(pipeline):
            stats.append({
                "client_name": result["_id"],
                "check_count": result["count"],
                "last_check": result["last_check"]
            })
        
        return {
            "total_clients": len(stats),
            "clients": stats
        }
