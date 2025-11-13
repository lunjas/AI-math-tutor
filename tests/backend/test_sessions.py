"""Tests for session management."""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.app.services.session_manager import SessionManager


def test_create_session():
    """Test session creation."""
    manager = SessionManager()
    session = manager.create_session()
    
    assert session is not None
    assert session.session_id is not None
    assert len(session.conversation_history) == 0


def test_get_session():
    """Test getting a session."""
    manager = SessionManager()
    session = manager.create_session()
    
    retrieved = manager.get_session(session.session_id)
    assert retrieved is not None
    assert retrieved.session_id == session.session_id


def test_get_nonexistent_session():
    """Test getting a non-existent session."""
    manager = SessionManager()
    session = manager.get_session("nonexistent-id")
    assert session is None


def test_add_message():
    """Test adding messages to a session."""
    manager = SessionManager()
    session = manager.create_session()
    
    session.add_message("user", "Hello")
    session.add_message("assistant", "Hi there!")
    
    assert len(session.conversation_history) == 2
    assert session.conversation_history[0]["role"] == "user"
    assert session.conversation_history[1]["role"] == "assistant"


def test_get_history():
    """Test getting conversation history."""
    manager = SessionManager()
    session = manager.create_session()
    
    session.add_message("user", "Message 1")
    session.add_message("assistant", "Response 1")
    session.add_message("user", "Message 2")
    
    history = session.get_history()
    assert len(history) == 3
    
    limited_history = session.get_history(limit=2)
    assert len(limited_history) == 2


def test_clear_history():
    """Test clearing conversation history."""
    manager = SessionManager()
    session = manager.create_session()
    
    session.add_message("user", "Hello")
    session.add_message("assistant", "Hi")
    
    assert len(session.conversation_history) == 2
    
    session.clear_history()
    assert len(session.conversation_history) == 0


def test_delete_session():
    """Test deleting a session."""
    manager = SessionManager()
    session = manager.create_session()
    session_id = session.session_id
    
    assert manager.get_session(session_id) is not None
    
    success = manager.delete_session(session_id)
    assert success is True
    assert manager.get_session(session_id) is None


def test_list_sessions():
    """Test listing all sessions."""
    manager = SessionManager()
    
    session1 = manager.create_session()
    session2 = manager.create_session()
    
    sessions = manager.list_sessions()
    assert len(sessions) >= 2
    
    session_ids = [s.session_id for s in sessions]
    assert session1.session_id in session_ids
    assert session2.session_id in session_ids


def test_get_or_create_session():
    """Test get_or_create_session method."""
    manager = SessionManager()
    
    # Create new session
    session1 = manager.get_or_create_session()
    assert session1 is not None
    
    # Get existing session
    session2 = manager.get_or_create_session(session1.session_id)
    assert session2.session_id == session1.session_id
    
    # Create new session with custom ID
    session3 = manager.get_or_create_session("custom-id")
    assert session3.session_id == "custom-id"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

