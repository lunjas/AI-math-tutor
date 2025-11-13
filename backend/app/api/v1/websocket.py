"""WebSocket endpoints for real-time streaming."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

from backend.app.services.tutor_service import tutor_service
from backend.app.services.session_manager import session_manager
from backend.app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for streaming chat responses.
    
    Expected message format:
    {
        "message": "user question",
        "session_id": "optional-session-id",
        "use_retrieval": true
    }
    
    Response format (streamed):
    {
        "type": "chunk",
        "content": "response chunk"
    }
    
    Final message:
    {
        "type": "done",
        "session_id": "session-id"
    }
    """
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                request = json.loads(data)
                message = request.get("message", "")
                session_id = request.get("session_id")
                use_retrieval = request.get("use_retrieval", True)
                
                if not message:
                    await websocket.send_json({
                        "type": "error",
                        "content": "Message cannot be empty"
                    })
                    continue
                
                # Get or create session
                session = session_manager.get_or_create_session(session_id)
                
                # Get conversation history
                history = session.get_history()
                
                # Stream the response
                full_response = ""
                async for chunk in tutor_service.ask_stream(
                    query=message,
                    use_retrieval=use_retrieval,
                    conversation_history=history
                ):
                    full_response += chunk
                    await websocket.send_json({
                        "type": "chunk",
                        "content": chunk
                    })
                
                # Add messages to session history
                session.add_message("user", message)
                session.add_message("assistant", full_response)
                
                # Send completion message
                await websocket.send_json({
                    "type": "done",
                    "session_id": session.session_id,
                    "message_count": len(session.conversation_history)
                })
                
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "content": "Invalid JSON format"
                })
            except Exception as e:
                logger.error(f"Error processing WebSocket message: {e}")
                await websocket.send_json({
                    "type": "error",
                    "content": str(e)
                })
                
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass

