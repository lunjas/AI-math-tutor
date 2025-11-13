"""Session management endpoints."""

from fastapi import APIRouter, HTTPException, status

from backend.app.models.session import (
    SessionCreate,
    SessionResponse,
    SessionListResponse,
    SessionDeleteResponse
)
from backend.app.services.session_manager import session_manager
from backend.app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/", response_model=SessionResponse)
async def create_session(request: SessionCreate = None):
    """Create a new session.
    
    Args:
        request: Optional session creation parameters
        
    Returns:
        Created session information
    """
    try:
        session = session_manager.create_session()
        return SessionResponse(
            session_id=session.session_id,
            created_at=session.created_at.isoformat(),
            message_count=len(session.conversation_history)
        )
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {str(e)}"
        )


@router.get("/", response_model=SessionListResponse)
async def list_sessions():
    """List all active sessions.
    
    Returns:
        List of sessions
    """
    try:
        sessions = session_manager.list_sessions()
        session_responses = [
            SessionResponse(
                session_id=s.session_id,
                created_at=s.created_at.isoformat(),
                message_count=len(s.conversation_history)
            )
            for s in sessions
        ]
        
        return SessionListResponse(
            sessions=session_responses,
            total=len(session_responses)
        )
    except Exception as e:
        logger.error(f"Error listing sessions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list sessions: {str(e)}"
        )


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """Get information about a specific session.
    
    Args:
        session_id: Session ID to retrieve
        
    Returns:
        Session information
    """
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    return SessionResponse(
        session_id=session.session_id,
        created_at=session.created_at.isoformat(),
        message_count=len(session.conversation_history)
    )


@router.delete("/{session_id}", response_model=SessionDeleteResponse)
async def delete_session(session_id: str):
    """Delete a session.
    
    Args:
        session_id: Session ID to delete
        
    Returns:
        Deletion result
    """
    success = session_manager.delete_session(session_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    return SessionDeleteResponse(
        success=True,
        message=f"Session {session_id} deleted successfully"
    )

