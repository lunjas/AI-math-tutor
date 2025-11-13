"""Pydantic models for quiz generation."""

from pydantic import BaseModel, Field


class QuizRequest(BaseModel):
    """Request model for quiz generation."""
    topic: str = Field(..., description="Topic to generate quiz questions about", min_length=1)
    num_questions: int = Field(3, description="Number of questions to generate", ge=1, le=10)
    session_id: str = Field(None, description="Optional session ID for context")


class QuizResponse(BaseModel):
    """Response model for quiz generation."""
    topic: str = Field(..., description="Topic of the quiz")
    questions: str = Field(..., description="Generated quiz questions")
    num_questions: int = Field(..., description="Number of questions generated")

