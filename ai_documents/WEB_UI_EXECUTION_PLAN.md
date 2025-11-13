# Web UI Implementation Plan for AI Math Tutor

## Executive Summary

This document outlines the comprehensive plan to extend the current CLI-based AI Math Tutor with a modern web interface using FastAPI as the backend API and Open WebUI as the frontend and all containerized with Docker for easy deployment.

---

## 📋 Current State Analysis

### Existing Architecture
- **Backend**: Python-based modular architecture
  - `TutorEngine`: Core RAG + reasoning logic
  - `VectorStore`: ChromaDB with Azure OpenAI embeddings
  - `MathTools`: SymPy symbolic computation
  - `DocumentProcessor`: PDF/TXT/MD parsing and chunking
  - `CLI`: Command-line interface

### Key Features
- RAG-based question answering
- Conversation history management
- Symbolic math computations
- Quiz generation
- Document ingestion
- Azure OpenAI integration (GPT-4o-mini, text-embedding-3-large)

### Technology Stack
- OpenAI API (Azure)
- ChromaDB (vector database)
- SymPy (symbolic math)
- PyMuPDF (document processing)
- Python 3.9+

---

## 🎯 Goals and Requirements

### Primary Objectives
1. **Create a FastAPI backend** that exposes all tutor functionality via REST API
2. **Integrate Open WebUI** for a modern chat interface
3. **Containerize the application** with Docker for easy deployment
4. **Maintain backward compatibility** with existing CLI interface
6. **Provide real-time streaming** for LLM responses
7. **Support document uploads** through the web interface

### Non-Functional Requirements
- **Performance**: Response time < 2 seconds for retrieval
- **Security**: API key protection, input validation
- **Maintainability**: Clear separation of concerns, comprehensive documentation
- **Deployment**: Single `docker-compose up` command to run entire stack

---

## 🏗️ Proposed Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Web Browser                              │
│                    (User Interface)                             │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/WebSocket
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Open WebUI Container                        │
│                      (Port 3000)                                │
│  • Chat interface                                               │
│  • Document upload UI                                           │
│  • Session management                                           │
│  • Real-time streaming                                          │
└────────────────────────────┬───────────────────────────────────┘
                             │ REST API / WebSocket
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend Container                     │
│                      (Port 8000)                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Routes Layer                       │  │
│  │  /api/v1/chat          - Chat endpoints                  │  │
│  │  /api/v1/compute       - Math computation                │  │
│  │  /api/v1/quiz          - Quiz generation                 │  │
│  │  /api/v1/documents     - Document management             │  │
│  │  /api/v1/sessions      - Session management              │  │
│  │  /ws/chat              - WebSocket for streaming         │  │
│  └────────────────────────────┬─────────────────────────────┘  │
│                               ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Business Logic Layer                         │  │
│  │  • SessionManager - Simple session handling              │  │
│  │  • TutorEngine - Existing core logic (enhanced)          │  │
│  │  • DocumentProcessor - File upload handling              │  │
│  │  • VectorStore - ChromaDB integration                    │  │
│  │  • MathTools - SymPy computations                        │  │
│  └────────────────────────────┬─────────────────────────────┘  │
│                               ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Data Layer                               │  │
│  │  • ChromaDB (vector embeddings)                          │  │
│  │  • Session store (in-memory)                             │  │
│  │  • File storage (uploaded documents)                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External Services                             │
│  • Azure OpenAI API (LLM + Embeddings)                          │
└─────────────────────────────────────────────────────────────────┘
```

### Component Overview

#### 1. FastAPI Backend Container
- **Purpose**: Expose all tutor functionality via REST API
- **Key Responsibilities**:
  - Handle HTTP requests and WebSocket connections
  - Manage user sessions
  - Orchestrate tutor engine operations
  - Stream LLM responses in real-time
  - Handle file uploads and processing

#### 2. Open WebUI Container
- **Purpose**: Modern chat interface for the tutor
- **Key Responsibilities**:
  - Render chat interface
  - Display math formulas (LaTeX/MathJax)
  - Handle file uploads
  - Show real-time streaming responses
  - Manage conversation history

#### 3. ChromaDB Storage
- **Purpose**: Persistent vector database
- **Implementation**:
  - Mount as volume in FastAPI container (simple)

#### 4. Session Storage (Optional)
- **Purpose**: Store user sessions across restarts
- **Implementation**:
  - In-memory (simple development setup)

---

## 📂 New Project Structure

```
AI_math_tutor/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI application entry point
│   │   ├── config.py                  # Enhanced config (from src/)
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py                # Pydantic models for chat
│   │   │   ├── compute.py             # Models for computation
│   │   │   ├── document.py            # Models for documents
│   │   │   └── session.py             # Models for sessions
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── routes.py          # Main API router
│   │   │   │   ├── chat.py            # Chat endpoints
│   │   │   │   ├── compute.py         # Computation endpoints
│   │   │   │   ├── quiz.py            # Quiz endpoints
│   │   │   │   ├── documents.py       # Document endpoints
│   │   │   │   ├── sessions.py        # Session endpoints (optional)
│   │   │   │   └── websocket.py       # WebSocket endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── session_manager.py     # Session management (optional)
│   │   │   ├── tutor_service.py       # Wrapper around TutorEngine
│   │   │   └── streaming.py           # Streaming response handler
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   └── error_handler.py       # Global error handling
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── logger.py              # Logging configuration
│   │       └── validators.py          # Input validation
│   ├── Dockerfile                      # FastAPI container
│   ├── requirements.txt               # Python dependencies
│   └── .env.example                   # Environment variables template
├── frontend/
│   ├── Dockerfile                     # Open WebUI container (if customized)
│   ├── config.json                    # Open WebUI configuration
│   └── custom_theme/                  # Custom styling (optional)
├── src/                               # Existing core modules (unchanged)
│   ├── __init__.py
│   ├── config.py                      # Original config
│   ├── tutor_engine.py                # Enhanced for streaming
│   ├── vector_store.py                # Enhanced for multi-user
│   ├── math_tools.py                  # Unchanged
│   ├── document_processor.py          # Enhanced for web uploads
│   └── cli.py                         # Kept for backward compatibility
├── data/
│   ├── documents/                     # Uploaded documents
│   ├── vector_db/                     # ChromaDB persistence
│   └── sessions/                      # Session data (if file-based)
├── docker-compose.yml                 # Orchestration configuration
├── docker-compose.dev.yml             # Development configuration
├── tests/
│   ├── backend/
│   │   ├── test_api.py
│   │   ├── test_sessions.py
│   │   └── test_streaming.py
│   └── integration/
│       └── test_end_to_end.py
├── scripts/
│   ├── init_db.py                     # Initialize vector database
│   ├── setup_env.sh                   # Environment setup
│   └── health_check.py                # Container health check
├── main.py                            # Original CLI entry point
├── requirements.txt                   # Original requirements
├── WEB_UI_EXECUTION_PLAN.md          # This document
├── ARCHITECTURE.md                    # Updated architecture docs
├── README.md                          # Updated with web UI instructions
└── .env                               # Environment variables (gitignored)
```

---

## 🔨 Implementation Plan

### Phase 1: FastAPI Backend Setup

#### Task 1.1: Project Structure & Dependencies

**Steps**:
1. Create `backend/` directory structure
2. Set up FastAPI application boilerplate
3. Update `requirements.txt` with web dependencies:
4. Create `.env.example` with all required variables:

**Deliverables**:
- Complete backend project structure
- Updated `requirements.txt`
- Configuration templates

---

#### Task 1.2: Pydantic Models

**Steps**:
1. Create request/response models in `backend/app/models/`

**Files to create**:

**`backend/app/models/chat.py`**:
**`backend/app/models/compute.py`**:
**`backend/app/models/document.py`**:
**`backend/app/models/session.py`**:

**Deliverables**:
- All Pydantic models for API contracts
- Input validation rules
- Response serialization models

---

#### Task 1.3: Session Management Service

**Steps**:
1. Create simple session manager

**File: `backend/app/services/session_manager.py`**:

**Deliverables**:
- Session management service

---

#### Task 1.4: Enhanced TutorEngine for Streaming

**Steps**:
1. Modify `TutorEngine` to support streaming responses
2. Create async wrapper methods
3. Add streaming generator functions

**File: `backend/app/services/tutor_service.py`**:

**Deliverables**:
- Streaming-enabled tutor service
- Async/await support
- Backward-compatible non-streaming methods

---

#### Task 1.5: API Routes Implementation
**Duration**: 3 days

**Steps**:
1. Implement all API endpoints
2. Add WebSocket support for streaming
3. Integrate session management
4. Add file upload handling

**Files to create**:
**`backend/app/main.py`**:
**`backend/app/api/v1/routes.py`**:
**`backend/app/api/v1/websocket.py`**:
**`backend/app/api/v1/compute.py`**:
**`backend/app/api/v1/documents.py`**:
**`backend/app/api/v1/sessions.py`**:

**Deliverables**:
- Complete FastAPI application
- All REST endpoints implemented
- WebSocket streaming support
- File upload functionality
- Session management integration

---

### Phase 2: Docker Configuration

#### Task 2.1: FastAPI Dockerfile

**File: `backend/Dockerfile`**:

**Deliverables**:
- Optimized Dockerfile for FastAPI
- Health check configuration

---

#### Task 2.2: Docker Compose Configuration

**Files to create**:
**`docker-compose.yml`**:
**`docker-compose.dev.yml`**:

**Deliverables**:
- Development `docker-compose.dev.yml`
- Network and volume configuration
- Environment variable management

---

#### Task 2.3: Environment & Scripts Setup

**Files to create**:
**`.env.example`**
**`scripts/setup_env.sh`**:
**`scripts/init_db.py`**:

**Deliverables**:
- Environment setup scripts
- Database initialization script
- Docker helper scripts

---

### Phase 3: Open WebUI Integration

#### Task 3.1: Open WebUI Configuration

**Research & Planning**:
1. Study Open WebUI documentation
2. Determine integration approach:
   - Use Open WebUI as-is with OpenAI-compatible API

**Steps**:
1. Configure Open WebUI to use custom backend
2. Create OpenAI-compatible endpoint adapter
3. Test chat interface integration

**File: `backend/app/api/v1/openai_compat.py`**:

**Deliverables**:
- OpenAI-compatible API adapter
- Open WebUI configuration
- Integration documentation

---

#### Task 3.2: Frontend Customization

**Optional customizations**:
1. Math formula rendering (MathJax/KaTeX)

**Deliverables**:
- Math rendering setup

---

### Phase 4: Testing & Documentation

#### Task 4.1: API Testing

**Files to create**:
**`tests/backend/test_api.py`**:
**`tests/integration/test_end_to_end.py`**:

**Deliverables**:
- Unit tests for all endpoints
- Integration tests
- Test coverage report

---

#### Task 4.2: Documentation Updates

**Files to update**:

1. **`README.md`**

**Deliverables**:
- Updated docs

---

#### Task 5.2: Monitoring & Logging

**File: `backend/app/utils/logger.py`**:
**Add to docker-compose.yml**:

**Deliverables**:
- Structured logging
- Log aggregation setup
- Performance monitoring

---

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Docker images built successfully
- [ ] Documentation complete

### Deployment Steps
1. Clone repository
2. Configure `.env` file
3. Run `./scripts/setup_env.sh`
4. Run `docker-compose up -d`
5. Run `python scripts/init_db.py` (if pre-loading documents)
6. Access http://localhost:3000
7. Verify all features working

### Post-Deployment
- [ ] Monitor logs for errors
- [ ] Test all endpoints
- [ ] Verify document upload
- [ ] Test streaming chat
- [ ] Check resource usage

---

## 🛠️ Technology Stack Summary

### Backend
- **Framework**: FastAPI 0.109+
- **ASGI Server**: Uvicorn
- **Database**: ChromaDB (vector)
- **AI**: Azure OpenAI (GPT-4o-mini, text-embedding-3-large)
- **Math**: SymPy
- **Document Processing**: PyMuPDF, tiktoken

### Frontend
- **UI**: Open WebUI

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Logging**: Python logging, JSON logs
- **Monitoring**: Docker stats, custom metrics

### Development Tools
- **API Testing**: pytest, httpx
- **Documentation**: FastAPI auto-docs, Markdown

---