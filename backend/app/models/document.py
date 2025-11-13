"""Pydantic models for document management endpoints."""

from typing import List
from pydantic import BaseModel, Field


class DocumentUploadResponse(BaseModel):
    """Response model for document upload."""
    success: bool = Field(..., description="Whether the upload was successful")
    filename: str = Field(..., description="Name of the uploaded file")
    chunks_created: int = Field(..., description="Number of chunks created from the document")
    message: str = Field(..., description="Status message")


class DocumentInfo(BaseModel):
    """Information about a document in the system."""
    filename: str = Field(..., description="Name of the document")
    chunks: int = Field(..., description="Number of chunks")
    source: str = Field(..., description="Source identifier")


class DocumentListResponse(BaseModel):
    """Response model for listing documents."""
    documents: List[DocumentInfo] = Field(..., description="List of documents in the system")
    total_chunks: int = Field(..., description="Total number of chunks across all documents")


class DocumentDeleteRequest(BaseModel):
    """Request model for deleting a document."""
    filename: str = Field(..., description="Name of the document to delete")


class DocumentDeleteResponse(BaseModel):
    """Response model for document deletion."""
    success: bool = Field(..., description="Whether the deletion was successful")
    message: str = Field(..., description="Status message")


class VectorStoreStats(BaseModel):
    """Statistics about the vector store."""
    total_chunks: int = Field(..., description="Total number of chunks in the vector store")
    collection_name: str = Field(..., description="Name of the ChromaDB collection")

