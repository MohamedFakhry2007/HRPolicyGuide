"""
Logger configuration for the HR Policy Chatbot.

This module sets up the logging system for the application.
"""

import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    """
    Configure the application logger.
    
    Sets up logging to both console and a file with appropriate formatting.
    """
    # Get log level from environment variable
    log_level_name = os.environ.get("LOG_LEVEL", "DEBUG")
    log_level = getattr(logging, log_level_name)
    
    # Get log file path from environment variable
    log_file = os.environ.get("LOG_FILE", "app.log")
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Create file handler for logging to a file
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10485760, backupCount=5
    )
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    
    # Add file handler to root logger
    logging.getLogger().addHandler(file_handler)
    
    # Log system info
    logger = logging.getLogger(__name__)
    logger.info("Logger initialized")
    logger.info(f"Log level: {log_level_name}")
    logger.info(f"Log file: {log_file}")
