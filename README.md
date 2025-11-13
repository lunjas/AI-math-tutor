# 🎓 AI Math Tutor

A personalized AI math tutor that uses **Retrieval-Augmented Generation (RAG)** and **symbolic computation** to help students learn mathematics from their own course materials. Available as both a **CLI** and **Web UI** with streaming chat interface.

This implementation has been done in cooperation with Cursor Agent (original prompt entered for the agent is in `EXECUTION_PLAN.md`).

## Features

✨ **Core Capabilities:**
- 📚 **Document Ingestion**: Import your course materials (PDF, TXT, MD)
- 🔍 **Smart Retrieval**: Find relevant information from your notes using semantic search
- 🤖 **AI Tutoring**: Get step-by-step explanations and guided learning
- 🔢 **Symbolic Math**: Accurate computations using SymPy
- 💬 **Interactive Q&A**: Natural conversation with context awareness
- 📝 **Quiz Generation**: Create practice problems on any topic
- 🌐 **Web Interface**: Modern chat UI with streaming responses (Open WebUI)
- 🐳 **Docker Support**: Easy deployment with Docker Compose
- 🔌 **REST API**: Full-featured FastAPI backend

## System Architecture

```
[Student Question]
       ↓
[Vector Search] → Retrieve relevant course material chunks
       ↓
[Context Builder] → Combine retrieved text + question + tutoring instructions
       ↓
[LLM Reasoner] → Generate pedagogical explanation
       ↓
[Math Tools] → Optional symbolic computation (SymPy)
       ↓
[Response] → Clear, educational answer
```

## Prerequisites

- **For Docker deployment** (recommended):
  - Docker and Docker Compose
  - Azure AI Foundry access (for Azure OpenAI API key and endpoint)

- **For CLI-only usage**:
  - Python 3.9 or higher
  - Azure AI Foundry access (for Azure OpenAI API key and endpoint)

## Quick Start (Docker - Recommended)

### 1. Setup Environment

```bash
# Run the setup script
./scripts/setup_env.sh

# Edit .env file with your Azure OpenAI credentials
nano .env  # or use your preferred editor
```

### 2. Start the Application

**Development mode** (with hot reload):
```bash
docker-compose -f docker-compose.dev.yml up
```

**Production mode**:
```bash
docker-compose up -d
```

### 3. Access the Application

- **Web UI**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API**: http://localhost:8000

### 4. Initialize with Documents (Optional)

```bash
# Copy your documents to data/documents/
cp ~/Documents/calculus_notes.pdf data/documents/

# Run initialization script
python scripts/init_db.py
```

### 5. Stop the Application

```bash
docker-compose down
```

## CLI Installation (Alternative)

If you prefer the command-line interface without Docker:

1. **Clone or download this repository**

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp backend/env.example .env
# Edit .env with your Azure OpenAI credentials
```

5. **Run the CLI tutor**:
```bash
python main.py
```

## Usage Guide

### Web UI Usage

The web interface provides a modern chat experience:

1. **Open http://localhost:3000** in your browser
2. **Start chatting** with the AI tutor
3. **Upload documents** using the document upload feature
4. **View conversation history** and manage sessions
5. **Get real-time streaming responses**

The web UI supports:
- Streaming chat responses
- Document upload and management
- Session management
- Math formula rendering
- Conversation history

### CLI Commands

#### 1. Ask Questions
```
ask <your question>
```
Examples:
- `ask What is the derivative of x^2?`
- `ask Explain the fundamental theorem of calculus`
- `What is integration by parts?` (you can omit 'ask')

#### 2. Symbolic Computation
```
compute <operation> <expression>
```

**Available Operations:**
- `simplify`: Simplify expressions
- `solve`: Solve equations
- `derivative`: Calculate derivatives
- `integral`: Calculate integrals
- `expand`: Expand expressions
- `factor`: Factor expressions

**Examples:**
```
compute simplify (x+1)*(x-1)
compute solve x**2 - 5*x + 6 = 0
compute derivative x**3 + 2*x**2 - x
compute integral sin(x)
compute expand (x+2)**3
compute factor x**2 - 4
```

#### 3. Generate Practice Problems
```
quiz <topic> [number_of_questions]
```
Examples:
- `quiz derivatives`
- `quiz integration 5`
- `quiz linear algebra 3`

#### 4. Ingest Documents
```
ingest <filepath>
```
Supported formats: PDF, TXT, MD

Examples:
- `ingest ~/Documents/lecture_notes.pdf`
- `ingest ./chapter3.txt`

#### 5. Other Commands
- `stats` - View knowledge base statistics
- `clear` - Clear conversation history
- `help` - Show help message
- `exit` - Exit the application

## Project Structure

```
AI_math_tutor/
├── main.py                      # CLI entry point
├── requirements.txt             # Core Python dependencies
├── docker-compose.yml           # Production Docker setup
├── docker-compose.dev.yml       # Development Docker setup
├── README.md                    # This file
├── QUICKSTART_WEB.md            # Instructions for web app startup
├── QUICKSTART.md                # Instructions for CLI app startup
├── ai_documents/                # AI prompts and summaries
├── backend/                     # FastAPI backend
│   ├── Dockerfile              # Backend container
│   ├── requirements.txt        # Backend dependencies
│   ├── env.example             # Environment template
│   └── app/
│       ├── main.py             # FastAPI application
│       ├── config.py           # Enhanced configuration
│       ├── models/             # Pydantic models
│       ├── api/v1/             # API routes
│       │   ├── chat.py         # Chat endpoints
│       │   ├── compute.py      # Math computation
│       │   ├── quiz.py         # Quiz generation
│       │   ├── documents.py    # Document management
│       │   ├── sessions.py     # Session management
│       │   ├── websocket.py    # WebSocket streaming
│       │   └── openai_compat.py # Open WebUI integration
│       ├── services/           # Business logic
│       │   ├── tutor_service.py    # Enhanced tutor
│       │   └── session_manager.py  # Session handling
│       ├── middleware/         # Middleware
│       └── utils/              # Utilities
├── src/                        # Core modules (shared)
│   ├── config.py              # Configuration management
│   ├── document_processor.py  # Document parsing
│   ├── vector_store.py        # Vector database (ChromaDB)
│   ├── math_tools.py          # Symbolic math (SymPy)
│   ├── tutor_engine.py        # Core tutor logic
│   └── cli.py                 # Command-line interface
├── scripts/                    # Utility scripts
│   ├── setup_env.sh           # Environment setup
│   ├── init_db.py             # Database initialization
│   └── health_check.py        # Health check
├── tests/                      # Test suite
│   ├── backend/               # Backend tests
│   └── integration/           # Integration tests
└── data/
    ├── documents/             # Course materials
    └── vector_db/             # Vector database storage
```

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | FastAPI |
| **Frontend UI** | Open WebUI |
| **Document Parsing** | PyMuPDF |
| **Vector Database** | ChromaDB |
| **Embeddings** | Azure OpenAI text-embedding-3-large |
| **LLM** | Azure OpenAI GPT-4o-mini |
| **Symbolic Math** | SymPy |
| **Text Processing** | tiktoken |
| **Containerization** | Docker, Docker Compose |
| **API Documentation** | FastAPI auto-docs (Swagger) |

## Configuration

Edit `.env` to customize settings:

```env
# API Keys
AZURE_OPENAI_ENDPOINT = your_azure_openai_endpoint
AZURE_OPENAI_API_KEY = your_azure_openai_api_key
AZURE_OPENAI_API_VERSION = your_azure_openai_api_version

# Model Configuration
EMBEDDING_MODEL=text-embedding-3-large
LLM_MODEL=gpt-4o-mini

# Paths
VECTOR_DB_PATH=./data/vector_db
DOCUMENTS_PATH=./data/documents

# Retrieval Settings
TOP_K_RESULTS=3        # Number of chunks to retrieve
CHUNK_SIZE=600         # Tokens per chunk
CHUNK_OVERLAP=100      # Overlap between chunks
```

## Example Session

```
🎓 AI Math Tutor - Your Personal Learning Assistant
============================================================

📚 You: ingest calculus_notes.pdf
📄 Processing document: calculus_notes.pdf...
Processed 'calculus_notes.pdf': 42 chunks created
✅ Successfully ingested 'calculus_notes.pdf'

📚 You: What is the derivative of x^2?

🤔 Thinking...

🎓 Tutor: Great question! Let me explain the derivative of x².

The derivative represents the rate of change. For f(x) = x², 
we can find the derivative using the power rule.

**Power Rule**: If f(x) = xⁿ, then f'(x) = n·xⁿ⁻¹

Applying this to x²:
- n = 2
- f'(x) = 2·x²⁻¹ = 2x

So, the derivative of x² is 2x.

This means that at any point x, the slope of the tangent line 
to the curve y = x² is 2x.

📚 You: compute derivative x**3 + 2*x

🔢 Computing...

=== Mathematical Computation ===
Operation: derivative
Input: x**3 + 2*x
Derivative: 3*x**2 + 2

📚 You: quiz derivatives 2

📝 Generating 2 practice problems on 'derivatives'...

[Quiz questions generated...]

📚 You: exit

👋 Goodbye! Happy learning!
```

## How It Works

### 1. Document Ingestion
- Documents are parsed (PDF/text extraction)
- Text is chunked into semantically meaningful segments (~600 tokens)
- Each chunk is embedded using OpenAI's embedding model
- Embeddings are stored in ChromaDB for fast retrieval

### 2. Question Answering
- Your question is embedded using the same model
- Similar chunks are retrieved from the vector database
- Retrieved context + your question are sent to GPT-4o-mini
- The LLM generates a pedagogical, step-by-step explanation

### 3. Symbolic Math
- SymPy handles exact mathematical computations
- Supports simplification, solving, calculus, algebra
- Provides verified, symbolic results

## Tips for Best Results

1. **Ingest Quality Materials**: The better your course materials, the better the answers
2. **Be Specific**: Ask clear, focused questions
3. **Use Compute for Verification**: Double-check calculations with symbolic math
4. **Generate Practice**: Use the quiz feature to test your understanding
5. **Iterate**: Follow up with clarifying questions

## API Endpoints

The FastAPI backend provides the following endpoints:

### Core Endpoints
- `POST /api/v1/chat/` - Send chat messages
- `POST /api/v1/compute/` - Perform mathematical computations
- `POST /api/v1/quiz/` - Generate practice quizzes
- `POST /api/v1/documents/upload` - Upload documents
- `GET /api/v1/documents/list` - List documents
- `GET /api/v1/documents/stats` - Vector store statistics

### Session Management
- `POST /api/v1/sessions/` - Create session
- `GET /api/v1/sessions/` - List sessions
- `GET /api/v1/sessions/{id}` - Get session
- `DELETE /api/v1/sessions/{id}` - Delete session

### WebSocket
- `WS /api/v1/ws/chat` - Streaming chat via WebSocket

### OpenAI-Compatible (for Open WebUI)
- `POST /api/v1/chat/completions` - OpenAI-compatible chat
- `GET /api/v1/models` - List available models

Full API documentation available at: http://localhost:8000/docs

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests
pytest tests/

# Run specific test file
pytest tests/backend/test_api.py -v

# Run with coverage
pytest tests/ --cov=backend --cov-report=html
```

## Troubleshooting

### Docker Issues

**Containers won't start**
- Check if ports 3000 and 8000 are available
- Verify Docker is running: `docker ps`
- Check logs: `docker-compose logs backend`

**API not connecting**
- Ensure `.env` file has correct Azure OpenAI credentials
- Check backend health: `python scripts/health_check.py`
- View backend logs: `docker-compose logs -f backend`

### CLI Issues

**Error: "AZURE_OPENAI_API_KEY not set"**
- Make sure you've created a `.env` file with your API key
- Check the `.env` file is in the project root

**No relevant materials found**
- Ensure you've ingested documents using the `ingest` command (CLI) or upload feature (Web UI)
- Check that your question relates to the ingested materials

**Import errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment

### Open WebUI Issues

**Can't access Web UI**
- Ensure Open WebUI container is running: `docker ps`
- Check if port 3000 is accessible
- Try accessing: http://localhost:3000

**Web UI can't connect to backend**
- Verify backend is healthy: http://localhost:8000/health
- Check Docker network: `docker network ls`
- Restart containers: `docker-compose restart`

## Architecture

See `ARCHITECTURE.md` for detailed system architecture and `WEB_UI_EXECUTION_PLAN.md` for web UI implementation details.

### High-Level Architecture

```
┌─────────────────────────────────────────┐
│         Web Browser (User)              │
└──────────────────┬──────────────────────┘
                   │ HTTP/WebSocket
                   ▼
┌─────────────────────────────────────────┐
│       Open WebUI Container              │
│         (Port 3000)                     │
└──────────────────┬──────────────────────┘
                   │ REST API
                   ▼
┌─────────────────────────────────────────┐
│    FastAPI Backend Container            │
│         (Port 8000)                     │
│  ┌─────────────────────────────────┐   │
│  │  API Routes                      │   │
│  │  - Chat, Compute, Quiz           │   │
│  │  - Documents, Sessions           │   │
│  │  - WebSocket, OpenAI-compat      │   │
│  └──────────────┬──────────────────┘   │
│                 ▼                        │
│  ┌─────────────────────────────────┐   │
│  │  Services                        │   │
│  │  - TutorService (RAG + LLM)     │   │
│  │  - SessionManager               │   │
│  │  - VectorStore (ChromaDB)       │   │
│  │  - MathTools (SymPy)            │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│      Azure OpenAI API                   │
│  - GPT-4o-mini (LLM)                   │
│  - text-embedding-3-large              │
└─────────────────────────────────────────┘
```

## Development

### Running in Development Mode

```bash
# Start with hot reload
docker-compose -f docker-compose.dev.yml up

# View logs
docker-compose -f docker-compose.dev.yml logs -f backend

# Rebuild after changes
docker-compose -f docker-compose.dev.yml up --build
```

### Making Changes

1. **Backend changes**: Edit files in `backend/app/`
2. **Core logic changes**: Edit files in `src/`
3. **Frontend changes**: Customize Open WebUI configuration

Changes are automatically reloaded in development mode.

## Future Enhancements

Potential additions:
- ✅ Web interface (completed with Open WebUI)
- ✅ REST API (completed with FastAPI)
- ✅ Docker deployment (completed)
- Support for more document formats (DOCX, HTML)
- Image/diagram recognition (OCR)
- Enhanced LaTeX rendering
- Export conversation history
- User authentication and profiles
- Spaced repetition for practice problems
- Mobile app
- Multi-language support

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to fork, modify, and submit pull requests!

---

**Happy Learning! 🎓📚**

