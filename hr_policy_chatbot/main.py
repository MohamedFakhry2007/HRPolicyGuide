"""
Main entry point for the HR Policy Chatbot application.

This module initializes and runs the Flask application.
"""

import logging
import os
from hr_policy_chatbot.app import app
from hr_policy_chatbot.logger import setup_logger
from hr_policy_chatbot.config import load_config
from hr_policy_chatbot.database import init_database
from hr_policy_chatbot.data.policies import populate_database


def main():
    """
    Initialize and run the application.
    
    Sets up logging, loads configuration, initializes database,
    and starts the Flask server.
    """
    # Setup logging
    setup_logger()
    logger = logging.getLogger(__name__)
    logger.info("Starting HR Policy Chatbot application")
    
    # Load configuration
    load_config()
    logger.info("Configuration loaded")
    
    # Initialize database
    init_database()
    logger.info("Database initialized")
    
    # Populate database with policy documents if it's empty
    populate_database()
    logger.info("Database populated with policy documents")
    
    # Run the Flask application
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting Flask application on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == "__main__":
    main()
