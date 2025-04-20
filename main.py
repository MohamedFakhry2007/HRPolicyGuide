"""
Main entry point for the HR Policy Chatbot application.

This module imports and exports the Flask application.
"""

import logging
from hr_policy_chatbot.app import app
from hr_policy_chatbot.logger import setup_logger
from hr_policy_chatbot.config import load_config
from hr_policy_chatbot.database import init_database
from hr_policy_chatbot.data.policies import populate_database
from hr_policy_chatbot.rag import initialize_retrieval_system

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

# Initialize retrieval system
initialize_retrieval_system()
logger.info("Retrieval system initialized")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)