"""
Data models for the HR Policy Chatbot.

This module defines the data structures used throughout the application.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class PolicyDocument(BaseModel):
    """Represents a policy document in the knowledge base."""
    
    id: Optional[int] = None
    title: str
    content: str
    created_at: Optional[datetime] = None
    
    class Config:
        """Configuration for the PolicyDocument model."""
        
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class RetrievedDocument(BaseModel):
    """Represents a document retrieved from the knowledge base."""
    
    id: int
    title: str
    content: str
    relevance_score: float


class UserQuery(BaseModel):
    """Represents a user's query to the chatbot."""
    
    message: str
    
    class Config:
        """Configuration for the UserQuery model."""
        
        json_schema_extra = {
            "example": {
                "message": "ما هي سياسة الإجازات السنوية؟"
            }
        }


class ChatResponse(BaseModel):
    """Represents the chatbot's response to a user query."""
    
    response: str
    relevant_docs: Optional[List[Dict]] = None
    
    class Config:
        """Configuration for the ChatResponse model."""
        
        json_schema_extra = {
            "example": {
                "response": "وفقًا لسياسة الشركة، يحق لكل موظف إجازة سنوية مدتها 30 يومًا..."
            }
        }
