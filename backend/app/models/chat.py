"""Pydantic models for chat endpoints."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Message(BaseModel):
    """A single message in a conversation."""
    role: str = Field(..., description="Role of the message sender (user/assistant/system)")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User's message/question", min_length=1)
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    use_retrieval: bool = Field(True, description="Whether to use RAG retrieval")
    stream: bool = Field(False, description="Whether to stream the response")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Assistant's response")
    session_id: str = Field(..., description="Session ID for this conversation")
    retrieved_chunks: Optional[List[Dict[str, Any]]] = Field(None, description="Retrieved context chunks")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ChatHistoryResponse(BaseModel):
    """Response model for chat history."""
    session_id: str
    messages: List[Message]
    created_at: str
    updated_at: str


class StreamChunk(BaseModel):
    """A chunk of streamed response."""
    content: str = Field(..., description="Chunk of the response")
    done: bool = Field(False, description="Whether this is the final chunk")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

