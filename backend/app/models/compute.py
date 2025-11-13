"""Pydantic models for computation endpoints."""

from typing import Optional, List
from pydantic import BaseModel, Field


class ComputeRequest(BaseModel):
    """Request model for mathematical computation."""
    expression: str = Field(..., description="Mathematical expression to compute", min_length=1)
    operation: str = Field(
        "simplify",
        description="Operation to perform: simplify, solve, derivative, integral, expand, factor"
    )
    variable: Optional[str] = Field(None, description="Variable for operations like solve, derivative, integral")
    order: Optional[int] = Field(None, description="Order for derivative operations")
    lower_bound: Optional[str] = Field(None, description="Lower bound for definite integrals")
    upper_bound: Optional[str] = Field(None, description="Upper bound for definite integrals")


class ComputeResponse(BaseModel):
    """Response model for mathematical computation."""
    success: bool = Field(..., description="Whether the computation was successful")
    operation: str = Field(..., description="Operation that was performed")
    original: Optional[str] = Field(None, description="Original expression")
    result: Optional[str] = Field(None, description="Computed result")
    latex: Optional[str] = Field(None, description="LaTeX representation of the result")
    error: Optional[str] = Field(None, description="Error message if computation failed")
    details: Optional[dict] = Field(None, description="Additional computation details")

