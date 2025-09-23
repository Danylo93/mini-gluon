"""
Base repository class with common database operations.
"""
from typing import Any, Dict, List, Optional, Type, TypeVar
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime

from app.core.database import database
from app.core.exceptions import DatabaseError, NotFoundError

T = TypeVar('T', bound=BaseModel)


class BaseRepository:
    """Base repository with common CRUD operations."""
    
    def __init__(self, collection_name: str, model_class: Type[T]):
        self.collection_name = collection_name
        self.model_class = model_class
        self._collection: Optional[AsyncIOMotorCollection] = None
    
    @property
    def collection(self) -> AsyncIOMotorCollection:
        """Get collection instance."""
        if not self._collection:
            db = database.get_database()
            self._collection = db[self.collection_name]
        return self._collection
    
    async def create(self, document: T) -> T:
        """Create a new document."""
        try:
            document_dict = document.dict()
            result = await self.collection.insert_one(document_dict)
            document_dict['_id'] = result.inserted_id
            return self.model_class(**document_dict)
        except Exception as e:
            raise DatabaseError(f"Failed to create document: {str(e)}")
    
    async def get_by_id(self, document_id: str) -> Optional[T]:
        """Get document by ID."""
        try:
            document = await self.collection.find_one({"_id": ObjectId(document_id)})
            if document:
                document['id'] = str(document['_id'])
                return self.model_class(**document)
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to get document by ID: {str(e)}")
    
    async def get_by_field(self, field: str, value: Any) -> Optional[T]:
        """Get document by field value."""
        try:
            document = await self.collection.find_one({field: value})
            if document:
                document['id'] = str(document['_id'])
                return self.model_class(**document)
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to get document by field: {str(e)}")
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[T]:
        """Get all documents with pagination."""
        try:
            filter_dict = filter_dict or {}
            cursor = self.collection.find(filter_dict).skip(skip).limit(limit)
            documents = []
            async for document in cursor:
                document['id'] = str(document['_id'])
                documents.append(self.model_class(**document))
            return documents
        except Exception as e:
            raise DatabaseError(f"Failed to get documents: {str(e)}")
    
    async def update(self, document_id: str, update_data: Dict[str, Any]) -> Optional[T]:
        """Update document by ID."""
        try:
            # Remove None values and add updated_at
            update_data = {k: v for k, v in update_data.items() if v is not None}
            update_data['updated_at'] = datetime.utcnow()
            
            result = await self.collection.update_one(
                {"_id": ObjectId(document_id)},
                {"$set": update_data}
            )
            
            if result.modified_count:
                return await self.get_by_id(document_id)
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to update document: {str(e)}")
    
    async def delete(self, document_id: str) -> bool:
        """Delete document by ID."""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(document_id)})
            return result.deleted_count > 0
        except Exception as e:
            raise DatabaseError(f"Failed to delete document: {str(e)}")
    
    async def count(self, filter_dict: Optional[Dict[str, Any]] = None) -> int:
        """Count documents."""
        try:
            filter_dict = filter_dict or {}
            return await self.collection.count_documents(filter_dict)
        except Exception as e:
            raise DatabaseError(f"Failed to count documents: {str(e)}")
    
    async def exists(self, filter_dict: Dict[str, Any]) -> bool:
        """Check if document exists."""
        try:
            count = await self.collection.count_documents(filter_dict, limit=1)
            return count > 0
        except Exception as e:
            raise DatabaseError(f"Failed to check document existence: {str(e)}")
