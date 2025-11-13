"""Main API router combining all v1 endpoints."""

from fastapi import APIRouter
from backend.app.api.v1 import chat, compute, quiz, documents, sessions, websocket, openai_compat

api_router = APIRouter()

# Include all sub-routers
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(compute.router, prefix="/compute", tags=["compute"])
api_router.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
api_router.include_router(openai_compat.router, tags=["openai-compatible"])


@api_router.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}

