"""
Flask application setup for the HR Policy Chatbot.

This module initializes the Flask application and defines all routes.
"""

import os
import logging
import json
from flask import Flask, render_template, request, jsonify

from hr_policy_chatbot.rag import retrieve_relevant_documents, generate_response

# Create Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Set up logger
logger = logging.getLogger(__name__)


@app.route("/")
def index():
    """
    Render the main chatbot interface.
    
    Returns:
        The rendered HTML template for the chat interface.
    """
    logger.debug("Rendering index page")
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Handle chat API requests.
    
    This endpoint receives user questions, processes them through the RAG system,
    and returns generated responses.
    
    Returns:
        JSON response containing the chatbot's answer.
    """
    try:
        logger.debug("Received chat request")
        data = request.get_json()
        
        if not data or "message" not in data:
            logger.warning("Invalid request: missing message field")
            return jsonify({"error": "Invalid request"}), 400
        
        user_message = data["message"]
        logger.info(f"User message: {user_message}")
        
        # Retrieve relevant documents based on the user's query
        relevant_docs = retrieve_relevant_documents(user_message)
        logger.debug(f"Retrieved {len(relevant_docs)} relevant documents")
        
        # Generate response using Gemini with retrieved documents as context
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(generate_response(user_message, relevant_docs))
        logger.info(f"Generated response: {response[:50]}...")
        
        return jsonify({"response": response})
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        return jsonify({"error": "An error occurred while processing your request"}), 500
