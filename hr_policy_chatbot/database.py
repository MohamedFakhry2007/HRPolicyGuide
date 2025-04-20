"""
Database management for the HR Policy Chatbot.

This module handles database connections and operations.
"""

import os
import sqlite3
import logging
from contextlib import contextmanager


# Set up logger
logger = logging.getLogger(__name__)

# Get database path from environment variable
db_path = os.environ.get("DATABASE_URL", "sqlite:///hr_policy_chatbot.db").replace("sqlite:///", "")


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    
    Yields:
        SQLite connection object.
    """
    conn = None
    try:
        logger.debug(f"Connecting to database at {db_path}")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}", exc_info=True)
        raise
    finally:
        if conn:
            logger.debug("Closing database connection")
            conn.close()


def init_database():
    """
    Initialize the database schema.
    
    Creates the necessary tables if they don't exist.
    """
    logger.info("Initializing database")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Create policy documents table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS policy_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create chat history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_message TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            logger.info("Database schema created successfully")
    
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {str(e)}", exc_info=True)
        raise


def get_all_policy_documents():
    """
    Retrieve all policy documents from the database.
    
    Returns:
        List of policy documents as dictionaries.
    """
    logger.debug("Retrieving all policy documents")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, content FROM policy_documents")
            documents = [dict(row) for row in cursor.fetchall()]
            logger.debug(f"Retrieved {len(documents)} policy documents")
            return documents
    
    except sqlite3.Error as e:
        logger.error(f"Error retrieving policy documents: {str(e)}", exc_info=True)
        return []


def add_policy_document(title, content):
    """
    Add a new policy document to the database.
    
    Args:
        title: The title of the policy document.
        content: The content of the policy document.
        
    Returns:
        The ID of the newly created document, or None if an error occurred.
    """
    logger.debug(f"Adding policy document: {title}")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO policy_documents (title, content) VALUES (?, ?)",
                (title, content)
            )
            conn.commit()
            document_id = cursor.lastrowid
            logger.info(f"Added policy document with ID {document_id}")
            return document_id
    
    except sqlite3.Error as e:
        logger.error(f"Error adding policy document: {str(e)}", exc_info=True)
        return None


def log_chat_interaction(user_message, bot_response):
    """
    Log a chat interaction to the database.
    
    Args:
        user_message: The message from the user.
        bot_response: The response from the bot.
        
    Returns:
        The ID of the newly created chat log entry, or None if an error occurred.
    """
    logger.debug("Logging chat interaction")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chat_history (user_message, bot_response) VALUES (?, ?)",
                (user_message, bot_response)
            )
            conn.commit()
            log_id = cursor.lastrowid
            logger.debug(f"Chat interaction logged with ID {log_id}")
            return log_id
    
    except sqlite3.Error as e:
        logger.error(f"Error logging chat interaction: {str(e)}", exc_info=True)
        return None
