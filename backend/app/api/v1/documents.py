"""Document management endpoints."""

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from pathlib import Path
import aiofiles
from typing import List

from backend.app.models.document import (
    DocumentUploadResponse,
    DocumentListResponse,
    DocumentInfo,
    VectorStoreStats
)
from backend.app.services.tutor_service import tutor_service
from backend.app.config import settings
from backend.app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document.
    
    Args:
        file: Document file to upload (PDF, TXT, or MD)
        
    Returns:
        Upload result with chunk count
    """
    try:
        # Validate file type
        allowed_extensions = {".pdf", ".txt", ".md"}
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file
        file_path = Path(settings.DOCUMENTS_PATH) / file.filename
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        logger.info(f"Saved uploaded file: {file.filename}")
        
        # Process document
        result = await tutor_service.process_document_async(str(file_path))
        
        return DocumentUploadResponse(
            success=result["success"],
            filename=result["filename"],
            chunks_created=result["chunks_created"],
            message=f"Document '{result['filename']}' processed successfully with {result['chunks_created']} chunks"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document: {str(e)}"
        )


@router.get("/list", response_model=DocumentListResponse)
async def list_documents():
    """List all documents in the system.
    
    Returns:
        List of documents with metadata
    """
    try:
        documents_path = Path(settings.DOCUMENTS_PATH)
        documents: List[DocumentInfo] = []
        
        if documents_path.exists():
            for file_path in documents_path.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in {".pdf", ".txt", ".md"}:
                    # Get chunk count from vector store
                    # This is a simplified version - in production you'd query the vector store
                    documents.append(DocumentInfo(
                        filename=file_path.name,
                        chunks=0,  # Would need to query vector store for accurate count
                        source=file_path.name
                    ))
        
        stats = tutor_service.get_vector_store_stats()
        
        return DocumentListResponse(
            documents=documents,
            total_chunks=stats.get("total_chunks", 0)
        )
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list documents: {str(e)}"
        )


@router.get("/stats", response_model=VectorStoreStats)
async def get_vector_store_stats():
    """Get vector store statistics.
    
    Returns:
        Vector store statistics
    """
    try:
        stats = tutor_service.get_vector_store_stats()
        return VectorStoreStats(
            total_chunks=stats.get("total_chunks", 0),
            collection_name=stats.get("collection_name", "unknown")
        )
    except Exception as e:
        logger.error(f"Error getting vector store stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )

