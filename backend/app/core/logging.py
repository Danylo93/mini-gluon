"""
Logging configuration for the application.
"""
import logging
import sys
from typing import Optional

from app.config.settings import settings


def setup_logging(log_level: Optional[str] = None) -> None:
    """
    Setup application logging configuration.
    
    Args:
        log_level: Override log level from settings
    """
    level = log_level or settings.log_level
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=settings.log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    # Configure specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("motor").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)
    
    # Create application logger
    logger = logging.getLogger("scaffold_forge")
    logger.info(f"Logging configured with level: {level}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f"scaffold_forge.{name}")
