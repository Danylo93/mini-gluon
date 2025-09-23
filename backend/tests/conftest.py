"""
Pytest configuration and fixtures.
"""
import pytest
import asyncio
from typing import AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import database
from app.config.settings import settings


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db() -> AsyncGenerator[AsyncIOMotorClient, None]:
    """Create a test database connection."""
    # Use a test database
    test_client = AsyncIOMotorClient(settings.mongo_url)
    test_db = test_client[f"{settings.db_name}_test"]
    
    yield test_db
    
    # Cleanup: drop test database
    await test_client.drop_database(f"{settings.db_name}_test")
    test_client.close()


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
async def mock_github_service():
    """Mock GitHub service for testing."""
    class MockGitHubService:
        async def create_repository(self, name: str, description: str, private: bool = False):
            return {
                "name": name,
                "full_name": f"test/{name}",
                "html_url": f"https://github.com/test/{name}",
                "clone_url": f"https://github.com/test/{name}.git",
                "ssh_url": f"git@github.com:test/{name}.git"
            }
        
        async def create_files(self, repo_name: str, files: dict, commit_message: str = "Initial commit"):
            return True
        
        async def test_connection(self):
            return True
    
    return MockGitHubService()
