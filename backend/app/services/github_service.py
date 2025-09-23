"""
GitHub service for repository operations.
"""
import time
from typing import Dict, List, Optional
from github import Github, GithubException
import logging

from app.config.settings import settings
from app.core.exceptions import GitHubError
from app.core.logging import get_logger

logger = get_logger(__name__)


class GitHubService:
    """Service for GitHub API operations."""
    
    def __init__(self):
        self.client = Github(settings.github_token)
        self._user = None
    
    @property
    def user(self):
        """Get authenticated user."""
        if not self._user:
            try:
                self._user = self.client.get_user()
            except GithubException as e:
                raise GitHubError(f"Failed to get GitHub user: {str(e)}")
        return self._user
    
    async def create_repository(
        self, 
        name: str, 
        description: str, 
        private: bool = False
    ) -> Dict[str, str]:
        """
        Create a new GitHub repository.
        
        Args:
            name: Repository name
            description: Repository description
            private: Whether repository should be private
            
        Returns:
            Dictionary with repository information
        """
        try:
            # Clean repository name
            repo_name = name.lower().replace(" ", "-").replace("_", "-")
            
            # Check if repository already exists
            try:
                existing_repo = self.user.get_repo(repo_name)
                if existing_repo:
                    raise GitHubError(f"Repository '{repo_name}' already exists")
            except GithubException:
                # Repository doesn't exist, which is what we want
                pass
            
            # Create repository
            repo = self.user.create_repo(
                name=repo_name,
                description=description,
                private=private,
                auto_init=False
            )
            
            logger.info(f"Created repository: {repo_name}")
            
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "html_url": repo.html_url,
                "clone_url": repo.clone_url,
                "ssh_url": repo.ssh_url
            }
            
        except GithubException as e:
            logger.error(f"GitHub API error: {str(e)}")
            raise GitHubError(f"Failed to create repository: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise GitHubError(f"Unexpected error creating repository: {str(e)}")
    
    async def create_files(
        self, 
        repo_name: str, 
        files: Dict[str, str],
        commit_message: str = "Initial commit"
    ) -> bool:
        """
        Create multiple files in a repository.
        
        Args:
            repo_name: Repository name
            files: Dictionary of file paths and contents
            commit_message: Commit message
            
        Returns:
            True if successful
        """
        try:
            repo = self.user.get_repo(repo_name)
            
            for file_path, content in files.items():
                try:
                    repo.create_file(
                        path=file_path,
                        message=f"{commit_message}: Add {file_path}",
                        content=content,
                        branch="main"
                    )
                    logger.debug(f"Created file: {file_path}")
                    
                    # Small delay to avoid rate limiting
                    time.sleep(0.5)
                    
                except GithubException as e:
                    logger.error(f"Failed to create file {file_path}: {str(e)}")
                    # Continue with other files
                    continue
            
            logger.info(f"Created {len(files)} files in repository {repo_name}")
            return True
            
        except GithubException as e:
            logger.error(f"GitHub API error: {str(e)}")
            raise GitHubError(f"Failed to create files: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise GitHubError(f"Unexpected error creating files: {str(e)}")
    
    async def get_repository(self, repo_name: str) -> Optional[Dict[str, str]]:
        """
        Get repository information.
        
        Args:
            repo_name: Repository name
            
        Returns:
            Repository information or None if not found
        """
        try:
            repo = self.user.get_repo(repo_name)
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "html_url": repo.html_url,
                "clone_url": repo.clone_url,
                "ssh_url": repo.ssh_url,
                "description": repo.description,
                "private": repo.private,
                "created_at": repo.created_at.isoformat(),
                "updated_at": repo.updated_at.isoformat()
            }
        except GithubException:
            return None
    
    async def delete_repository(self, repo_name: str) -> bool:
        """
        Delete a repository.
        
        Args:
            repo_name: Repository name
            
        Returns:
            True if successful
        """
        try:
            repo = self.user.get_repo(repo_name)
            repo.delete()
            logger.info(f"Deleted repository: {repo_name}")
            return True
        except GithubException as e:
            logger.error(f"Failed to delete repository: {str(e)}")
            raise GitHubError(f"Failed to delete repository: {str(e)}")
    
    async def test_connection(self) -> bool:
        """
        Test GitHub API connection.
        
        Returns:
            True if connection is successful
        """
        try:
            self.user.get_repo("test")  # This will fail but test the connection
            return True
        except GithubException as e:
            if e.status == 404:
                # Repository not found, but connection is working
                return True
            return False
        except Exception:
            return False
