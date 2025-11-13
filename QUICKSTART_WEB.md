# 🚀 Quick Start Guide - Web UI

Get the AI Math Tutor web interface up and running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- Azure OpenAI API credentials (API key and endpoint)

## Step-by-Step Setup

### 1. Get Your Azure OpenAI Credentials

You'll need:
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_VERSION` (usually `2024-02-15-preview`)

Get these from your Azure AI Foundry portal.

### 2. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd AI_math_tutor

# Run the setup script
./scripts/setup_env.sh
```

### 3. Configure Environment

Edit the `.env` file that was created:

```bash
nano .env  # or use your preferred editor
```

Update these values:
```env
AZURE_OPENAI_API_KEY=your-actual-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

Save and close the file.

### 4. Start the Application

```bash
# Start in production mode
docker-compose up -d

# Or start in development mode (with hot reload)
docker-compose -f docker-compose.dev.yml up
```

Wait for the containers to start (about 30-60 seconds).

### 5. Verify Everything is Running

```bash
# Check container status
docker ps

# Run health check
python scripts/health_check.py
```

You should see two containers running:
- `ai-math-tutor-backend` (port 8000)
- `ai-math-tutor-webui` (port 3000)

### 6. Access the Application

Open your browser and go to:

- **Web UI**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## First Steps in the Web UI

### 1. Upload Course Materials

1. Click on the **document upload** icon in the web UI
2. Select a PDF, TXT, or MD file with your course materials
3. Wait for processing to complete
4. Your documents are now searchable!

### 2. Start Chatting

Simply type your question in the chat box:

- "What is the chain rule?"
- "Explain how to solve quadratic equations"
- "Help me understand integration by parts"

The AI tutor will retrieve relevant information from your documents and provide step-by-step explanations.

### 3. Use Math Computations

You can ask for symbolic computations:

- "Simplify (x+1)(x-1)"
- "Solve x^2 - 5x + 6 = 0"
- "Find the derivative of x^3 + 2x"
- "Integrate sin(x)"

### 4. Generate Practice Quizzes

Ask for practice problems:

- "Generate a quiz on derivatives with 3 questions"
- "Create practice problems about integration"
- "Give me exercises on linear algebra"

## Using the API Directly

### Chat Endpoint

```bash
curl -X POST "http://localhost:8000/api/v1/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the derivative of x^2?",
    "use_retrieval": true
  }'
```

### Compute Endpoint

```bash
curl -X POST "http://localhost:8000/api/v1/compute/" \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "x**2 + 2*x + 1",
    "operation": "simplify"
  }'
```

### Upload Document

```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@/path/to/your/document.pdf"
```

## Stopping the Application

```bash
# Stop containers (production)
docker-compose down

# Stop containers (development)
docker-compose -f docker-compose.dev.yml down

# Stop and remove all data
docker-compose down -v
```

## Troubleshooting

### Containers won't start

```bash
# Check logs
docker-compose logs backend
docker-compose logs open-webui

# Restart containers
docker-compose restart
```

### Can't access the Web UI

1. Verify containers are running: `docker ps`
2. Check if port 3000 is available: `lsof -i :3000` (Mac/Linux)
3. Try accessing directly: http://127.0.0.1:3000

### Backend not responding

1. Check backend health: http://localhost:8000/health
2. Verify API credentials in `.env`
3. View backend logs: `docker-compose logs -f backend`

### Document upload fails

1. Check file format (PDF, TXT, or MD only)
2. Ensure file size is reasonable (< 50MB)
3. Check backend logs for errors

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [WEB_UI_EXECUTION_PLAN.md](WEB_UI_EXECUTION_PLAN.md) for architecture details
- Explore the API documentation at http://localhost:8000/docs
- Run tests: `pytest tests/`

## Getting Help

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify your Azure OpenAI credentials
3. Ensure Docker is running properly
4. Check that ports 3000 and 8000 are available

## Tips for Best Results

1. **Upload quality materials**: The better your course documents, the better the answers
2. **Be specific**: Ask clear, focused questions
3. **Use retrieval**: Enable RAG for questions about your materials
4. **Verify computations**: Use the compute endpoint for exact calculations
5. **Practice regularly**: Generate quizzes to test your understanding

---

**Happy Learning! 🎓📚**

For more information, see the full [README.md](README.md).

