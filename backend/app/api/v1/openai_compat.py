"""OpenAI-compatible API endpoints for Open WebUI integration."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, AsyncGenerator
import json
import time
import uuid

from backend.app.services.tutor_service import tutor_service
from backend.app.services.session_manager import session_manager
from backend.app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


class OpenAIMessage(BaseModel):
    """OpenAI-compatible message format."""
    role: str
    content: str


class OpenAIChatRequest(BaseModel):
    """OpenAI-compatible chat completion request."""
    model: str = Field(default="gpt-4o-mini")
    messages: List[OpenAIMessage]
    stream: bool = Field(default=False)
    temperature: Optional[float] = Field(default=0.7)
    max_tokens: Optional[int] = Field(default=2000)
    # Custom fields for our tutor
    use_retrieval: bool = Field(default=True)
    session_id: Optional[str] = Field(default=None)


class OpenAIChatResponse(BaseModel):
    """OpenAI-compatible chat completion response."""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Optional[Dict[str, int]] = None


@router.post("/chat/completions")
async def chat_completions(request: OpenAIChatRequest):
    """OpenAI-compatible chat completions endpoint.
    
    This endpoint mimics the OpenAI API format to work with Open WebUI.
    
    Args:
        request: OpenAI-compatible chat request
        
    Returns:
        OpenAI-compatible response or streaming response
    """
    try:
        # Extract the last user message
        user_messages = [msg for msg in request.messages if msg.role == "user"]
        if not user_messages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No user message found in request"
            )
        
        last_message = user_messages[-1].content
        
        # Get or create session
        session = session_manager.get_or_create_session(request.session_id)
        
        # Build conversation history from messages (excluding system messages)
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages[:-1]  # Exclude the last message
            if msg.role in ["user", "assistant"]
        ]
        
        if request.stream:
            # Return streaming response
            return StreamingResponse(
                stream_chat_response(
                    message=last_message,
                    session=session,
                    history=history,
                    use_retrieval=request.use_retrieval,
                    model=request.model
                ),
                media_type="text/event-stream"
            )
        else:
            # Return non-streaming response
            response = await tutor_service.ask_async(
                query=last_message,
                use_retrieval=request.use_retrieval,
                conversation_history=history
            )
            
            # Update session
            session.add_message("user", last_message)
            session.add_message("assistant", response)
            
            # Build OpenAI-compatible response
            completion_id = f"chatcmpl-{uuid.uuid4().hex[:8]}"
            
            return OpenAIChatResponse(
                id=completion_id,
                object="chat.completion",
                created=int(time.time()),
                model=request.model,
                choices=[
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": response
                        },
                        "finish_reason": "stop"
                    }
                ],
                usage={
                    "prompt_tokens": 0,  # Would need to calculate
                    "completion_tokens": 0,  # Would need to calculate
                    "total_tokens": 0
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat completions endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat completion: {str(e)}"
        )


async def stream_chat_response(
    message: str,
    session: Any,
    history: List[Dict[str, str]],
    use_retrieval: bool,
    model: str
) -> AsyncGenerator[str, None]:
    """Stream chat response in OpenAI format.
    
    Args:
        message: User message
        session: Session object
        history: Conversation history
        use_retrieval: Whether to use RAG
        model: Model name
        
    Yields:
        Server-sent event formatted chunks
    """
    completion_id = f"chatcmpl-{uuid.uuid4().hex[:8]}"
    created = int(time.time())
    
    full_response = ""
    
    try:
        async for chunk in tutor_service.ask_stream(
            query=message,
            use_retrieval=use_retrieval,
            conversation_history=history
        ):
            full_response += chunk
            
            # Format as OpenAI streaming response
            chunk_data = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "content": chunk
                        },
                        "finish_reason": None
                    }
                ]
            }
            
            yield f"data: {json.dumps(chunk_data)}\n\n"
        
        # Update session
        session.add_message("user", message)
        session.add_message("assistant", full_response)
        
        # Send final chunk
        final_chunk = {
            "id": completion_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "delta": {},
                    "finish_reason": "stop"
                }
            ]
        }
        
        yield f"data: {json.dumps(final_chunk)}\n\n"
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        logger.error(f"Error in streaming: {e}")
        error_chunk = {
            "error": {
                "message": str(e),
                "type": "server_error"
            }
        }
        yield f"data: {json.dumps(error_chunk)}\n\n"


@router.get("/models")
async def list_models():
    """List available models (OpenAI-compatible).
    
    Returns:
        List of available models
    """
    return {
        "object": "list",
        "data": [
            {
                "id": "ai-math-tutor",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "ai-math-tutor",
                "permission": [],
                "root": "ai-math-tutor",
                "parent": None
            },
            {
                "id": "gpt-4o-mini",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "ai-math-tutor",
                "permission": [],
                "root": "gpt-4o-mini",
                "parent": None
            }
        ]
    }

