"""Pydantic models for session management."""

from typing import List, Optional
from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    """Request model for creating a new session."""
    user_id: Optional[str] = Field(None, description="Optional user identifier")


class SessionResponse(BaseModel):
    """Response model for session operations."""
    session_id: str = Field(..., description="Unique session identifier")
    created_at: str = Field(..., description="Session creation timestamp")
    message_count: int = Field(0, description="Number of messages in the session")


class SessionListResponse(BaseModel):
    """Response model for listing sessions."""
    sessions: List[SessionResponse] = Field(..., description="List of active sessions")
    total: int = Field(..., description="Total number of sessions")


class SessionDeleteResponse(BaseModel):
    """Response model for session deletion."""
    success: bool = Field(..., description="Whether the deletion was successful")
    message: str = Field(..., description="Status message")

