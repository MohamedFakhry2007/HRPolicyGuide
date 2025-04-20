"""
Main entry point for the HR Policy Chatbot application.

This module imports and exports the Flask application.
"""

from hr_policy_chatbot.app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)