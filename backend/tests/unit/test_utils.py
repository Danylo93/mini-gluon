"""
Unit tests for utility functions.
"""
import pytest

from app.utils.validators import (
    validate_project_name,
    validate_github_username,
    validate_repository_name,
    validate_url,
    sanitize_filename,
    validate_template_variables,
    validate_pagination_params
)


class TestProjectNameValidation:
    """Test project name validation."""
    
    def test_valid_project_names(self):
        """Test valid project names."""
        valid_names = [
            "my-project",
            "my_project",
            "My Project",
            "project123",
            "a",
            "a" * 100
        ]
        
        for name in valid_names:
            assert validate_project_name(name), f"Should be valid: {name}"
    
    def test_invalid_project_names(self):
        """Test invalid project names."""
        invalid_names = [
            "",
            "a" * 101,  # Too long
            "project@name",  # Invalid character
            "project#name",  # Invalid character
            "project/name",  # Invalid character
        ]
        
        for name in invalid_names:
            assert not validate_project_name(name), f"Should be invalid: {name}"


class TestGitHubUsernameValidation:
    """Test GitHub username validation."""
    
    def test_valid_usernames(self):
        """Test valid GitHub usernames."""
        valid_usernames = [
            "user",
            "user123",
            "user-name",
            "a",
            "a" * 39
        ]
        
        for username in valid_usernames:
            assert validate_github_username(username), f"Should be valid: {username}"
    
    def test_invalid_usernames(self):
        """Test invalid GitHub usernames."""
        invalid_usernames = [
            "",
            "a" * 40,  # Too long
            "-user",  # Starts with hyphen
            "user-",  # Ends with hyphen
            "user_name",  # Underscore not allowed
            "user@name",  # Invalid character
        ]
        
        for username in invalid_usernames:
            assert not validate_github_username(username), f"Should be invalid: {username}"


class TestRepositoryNameValidation:
    """Test repository name validation."""
    
    def test_valid_repository_names(self):
        """Test valid repository names."""
        valid_names = [
            "repo",
            "repo123",
            "repo-name",
            "repo.name",
            "repo_name",
            "a",
            "a" * 100
        ]
        
        for name in valid_names:
            assert validate_repository_name(name), f"Should be valid: {name}"
    
    def test_invalid_repository_names(self):
        """Test invalid repository names."""
        invalid_names = [
            "",
            "a" * 101,  # Too long
            "repo@name",  # Invalid character
            "repo#name",  # Invalid character
            "repo/name",  # Invalid character
        ]
        
        for name in invalid_names:
            assert not validate_repository_name(name), f"Should be invalid: {name}"


class TestURLValidation:
    """Test URL validation."""
    
    def test_valid_urls(self):
        """Test valid URLs."""
        valid_urls = [
            "https://github.com/user/repo",
            "http://example.com",
            "https://api.github.com",
            "ftp://files.example.com"
        ]
        
        for url in valid_urls:
            assert validate_url(url), f"Should be valid: {url}"
    
    def test_invalid_urls(self):
        """Test invalid URLs."""
        invalid_urls = [
            "",
            "not-a-url",
            "github.com/user/repo",  # Missing scheme
            "https://",  # Missing host
        ]
        
        for url in invalid_urls:
            assert not validate_url(url), f"Should be invalid: {url}"


class TestFilenameSanitization:
    """Test filename sanitization."""
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        test_cases = [
            ("normal-file.txt", "normal-file.txt"),
            ("file<with>bad:chars", "file_with_bad_chars"),
            ("file/with\\slashes", "file_with_slashes"),
            ("  spaced  ", "spaced"),
            ("", "unnamed"),
            ("...", "unnamed"),
        ]
        
        for input_name, expected in test_cases:
            result = sanitize_filename(input_name)
            assert result == expected, f"Expected {expected}, got {result}"


class TestTemplateVariableValidation:
    """Test template variable validation."""
    
    def test_valid_variables(self):
        """Test valid template variables."""
        template_vars = {"project_name": "string", "description": "string"}
        provided_vars = {"project_name": "my-project", "description": "A test project"}
        
        errors = validate_template_variables(template_vars, provided_vars)
        assert len(errors) == 0, f"Should be valid, got errors: {errors}"
    
    def test_missing_variables(self):
        """Test missing required variables."""
        template_vars = {"project_name": "string", "description": "string"}
        provided_vars = {"project_name": "my-project"}
        
        errors = validate_template_variables(template_vars, provided_vars)
        assert len(errors) == 1
        assert "Missing required variables" in errors[0]
    
    def test_extra_variables(self):
        """Test extra variables."""
        template_vars = {"project_name": "string"}
        provided_vars = {"project_name": "my-project", "extra_var": "value"}
        
        errors = validate_template_variables(template_vars, provided_vars)
        assert len(errors) == 1
        assert "Unknown variables" in errors[0]
    
    def test_invalid_variable_types(self):
        """Test invalid variable types."""
        template_vars = {"project_name": "string"}
        provided_vars = {"project_name": 123}  # Should be string
        
        errors = validate_template_variables(template_vars, provided_vars)
        assert len(errors) == 1
        assert "must be a string" in errors[0]


class TestPaginationValidation:
    """Test pagination parameter validation."""
    
    def test_valid_pagination(self):
        """Test valid pagination parameters."""
        errors = validate_pagination_params(0, 10)
        assert len(errors) == 0, f"Should be valid, got errors: {errors}"
    
    def test_invalid_skip(self):
        """Test invalid skip parameter."""
        errors = validate_pagination_params(-1, 10)
        assert len(errors) == 1
        assert "Skip parameter must be non-negative" in errors[0]
    
    def test_invalid_limit(self):
        """Test invalid limit parameter."""
        errors = validate_pagination_params(0, 0)
        assert len(errors) == 1
        assert "Limit parameter must be at least 1" in errors[0]
        
        errors = validate_pagination_params(0, 1001)
        assert len(errors) == 1
        assert "Limit parameter cannot exceed 1000" in errors[0]
