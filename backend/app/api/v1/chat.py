"""Chat endpoints for conversational interactions."""

from fastapi import APIRouter, HTTPException, status
from backend.app.models.chat import ChatRequest, ChatResponse, ChatHistoryResponse
from backend.app.services.tutor_service import tutor_service
from backend.app.services.session_manager import session_manager
from backend.app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to the tutor and get a response.
    
    Args:
        request: Chat request with message and optional session ID
        
    Returns:
        Chat response with tutor's answer
    """
    try:
        # Get or create session
        session = session_manager.get_or_create_session(request.session_id)
        
        # Get conversation history from session
        history = session.get_history()
        
        # Get response from tutor
        response = await tutor_service.ask_async(
            query=request.message,
            use_retrieval=request.use_retrieval,
            conversation_history=history
        )
        
        # Add messages to session history
        session.add_message("user", request.message)
        session.add_message("assistant", response)
        
        # Get retrieved chunks if retrieval was used
        retrieved_chunks = None
        if request.use_retrieval:
            results = tutor_service.vector_store.query(request.message)
            if results and results.get("documents") and results["documents"][0]:
                retrieved_chunks = [
                    {
                        "text": doc,
                        "metadata": meta
                    }
                    for doc, meta in zip(
                        results["documents"][0],
                        results.get("metadatas", [[]])[0]
                    )
                ]
        
        return ChatResponse(
            response=response,
            session_id=session.session_id,
            retrieved_chunks=retrieved_chunks,
            metadata={
                "use_retrieval": request.use_retrieval,
                "message_count": len(session.conversation_history)
            }
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat request: {str(e)}"
        )


@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(session_id: str):
    """Get chat history for a session.
    
    Args:
        session_id: Session ID to retrieve history for
        
    Returns:
        Chat history
    """
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    return ChatHistoryResponse(
        session_id=session.session_id,
        messages=[
            {"role": msg["role"], "content": msg["content"]}
            for msg in session.conversation_history
        ],
        created_at=session.created_at.isoformat(),
        updated_at=session.updated_at.isoformat()
    )


@router.delete("/history/{session_id}")
async def clear_chat_history(session_id: str):
    """Clear chat history for a session.
    
    Args:
        session_id: Session ID to clear history for
        
    Returns:
        Success message
    """
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    session.clear_history()
    return {"message": f"Chat history cleared for session {session_id}"}

