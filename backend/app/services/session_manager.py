"""Session management service for handling user sessions."""

import uuid
from typing import Dict, List, Optional
from datetime import datetime
from backend.app.utils.logger import setup_logger

logger = setup_logger(__name__)


class Session:
    """Represents a user session with conversation history."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.conversation_history: List[Dict[str, str]] = []
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history.
        
        Args:
            role: Role of the message sender (user/assistant/system)
            content: Content of the message
        """
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        self.updated_at = datetime.now()
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """Get conversation history.
        
        Args:
            limit: Maximum number of recent messages to return
            
        Returns:
            List of messages
        """
        if limit:
            return self.conversation_history[-limit:]
        return self.conversation_history
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert session to dictionary representation."""
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "message_count": len(self.conversation_history),
            "messages": self.conversation_history
        }


class SessionManager:
    """Manages user sessions in memory."""
    
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        logger.info("SessionManager initialized")
    
    def create_session(self, session_id: Optional[str] = None) -> Session:
        """Create a new session.
        
        Args:
            session_id: Optional custom session ID
            
        Returns:
            Created session
        """
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        if session_id in self.sessions:
            logger.warning(f"Session {session_id} already exists, returning existing session")
            return self.sessions[session_id]
        
        session = Session(session_id)
        self.sessions[session_id] = session
        logger.info(f"Created new session: {session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get an existing session.
        
        Args:
            session_id: Session ID to retrieve
            
        Returns:
            Session if found, None otherwise
        """
        return self.sessions.get(session_id)
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> Session:
        """Get an existing session or create a new one.
        
        Args:
            session_id: Optional session ID
            
        Returns:
            Session instance
        """
        if session_id and session_id in self.sessions:
            return self.sessions[session_id]
        return self.create_session(session_id)
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session.
        
        Args:
            session_id: Session ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Deleted session: {session_id}")
            return True
        logger.warning(f"Attempted to delete non-existent session: {session_id}")
        return False
    
    def list_sessions(self) -> List[Session]:
        """List all active sessions.
        
        Returns:
            List of all sessions
        """
        return list(self.sessions.values())
    
    def clear_all_sessions(self):
        """Clear all sessions."""
        count = len(self.sessions)
        self.sessions.clear()
        logger.info(f"Cleared all {count} sessions")
    
    def get_session_count(self) -> int:
        """Get the number of active sessions.
        
        Returns:
            Number of sessions
        """
        return len(self.sessions)


# Global session manager instance
session_manager = SessionManager()

