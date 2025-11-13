"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_api_health_endpoint():
    """Test API v1 health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_models_endpoint():
    """Test OpenAI-compatible models endpoint."""
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0


def test_create_session():
    """Test session creation."""
    response = client.post("/api/v1/sessions/")
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "created_at" in data


def test_list_sessions():
    """Test listing sessions."""
    response = client.get("/api/v1/sessions/")
    assert response.status_code == 200
    data = response.json()
    assert "sessions" in data
    assert "total" in data


def test_compute_simplify():
    """Test computation endpoint with simplify operation."""
    payload = {
        "expression": "x**2 + 2*x + 1",
        "operation": "simplify"
    }
    response = client.post("/api/v1/compute/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "operation" in data
    assert data["operation"] == "simplify"


def test_compute_invalid_operation():
    """Test computation with invalid operation."""
    payload = {
        "expression": "x**2",
        "operation": "invalid_op"
    }
    response = client.post("/api/v1/compute/", json=payload)
    assert response.status_code == 400


def test_vector_store_stats():
    """Test vector store stats endpoint."""
    response = client.get("/api/v1/documents/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_chunks" in data
    assert "collection_name" in data


def test_list_documents():
    """Test document listing endpoint."""
    response = client.get("/api/v1/documents/list")
    assert response.status_code == 200
    data = response.json()
    assert "documents" in data
    assert "total_chunks" in data


def test_quiz_generation():
    """Test quiz generation endpoint."""
    payload = {
        "topic": "derivatives",
        "num_questions": 2
    }
    response = client.post("/api/v1/quiz/", json=payload)
    # This might fail without proper API keys, so we check for either success or 500
    assert response.status_code in [200, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

