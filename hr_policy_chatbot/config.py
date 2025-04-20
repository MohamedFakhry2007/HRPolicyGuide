"""
Configuration management for the HR Policy Chatbot.

This module loads configuration from environment variables using dotenv.
"""

import os
import logging
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    gemini_api_key: str
    
    # Application settings
    session_secret: str = "default-secret-key"
    log_level: str = "DEBUG"
    log_file: str = "app.log"
    
    # Database settings
    database_url: str = "sqlite:///hr_policy_chatbot.db"


def load_config():
    """
    Load configuration from .env file and environment variables.
    
    Returns:
        Settings object containing application configuration.
    """
    logger = logging.getLogger(__name__)
    logger.info("Loading configuration")
    
    # Load .env file if it exists
    load_dotenv()
    
    try:
        settings = Settings(
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            session_secret=os.getenv("SESSION_SECRET", "default-secret-key"),
            log_level=os.getenv("LOG_LEVEL", "DEBUG"),
            log_file=os.getenv("LOG_FILE", "app.log"),
            database_url=os.getenv("DATABASE_URL", "sqlite:///hr_policy_chatbot.db"),
        )
        
        # Set environment variables for other modules to use
        os.environ["SESSION_SECRET"] = settings.session_secret
        os.environ["LOG_LEVEL"] = settings.log_level
        os.environ["LOG_FILE"] = settings.log_file
        os.environ["DATABASE_URL"] = settings.database_url
        
        logger.info("Configuration loaded successfully")
        
        # Validate required settings
        if not settings.gemini_api_key:
            logger.error("GEMINI_API_KEY not set in environment variables")
            raise ValueError("GEMINI_API_KEY is required")
        
        return settings
    
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}", exc_info=True)
        raise
