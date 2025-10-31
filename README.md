# 🎓 AI Math Tutor

A personalized AI math tutor that uses **Retrieval-Augmented Generation (RAG)** and **symbolic computation** to help students learn mathematics from their own course materials.

## Features

✨ **Core Capabilities:**
- 📚 **Document Ingestion**: Import your course materials (PDF, TXT, MD)
- 🔍 **Smart Retrieval**: Find relevant information from your notes using semantic search
- 🤖 **AI Tutoring**: Get step-by-step explanations and guided learning
- 🔢 **Symbolic Math**: Accurate computations using SymPy
- 💬 **Interactive Q&A**: Natural conversation with context awareness
- 📝 **Quiz Generation**: Create practice problems on any topic

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

- Python 3.8 or higher
- OpenAI API key

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=sk-your-key-here
     ```

## Quick Start

1. **Run the tutor**:
```bash
python main.py
```

2. **Ingest your course materials**:
```
📚 You: ingest ~/Documents/calculus_notes.pdf
```

3. **Start learning**:
```
📚 You: What is the chain rule?
📚 You: ask Explain how to find derivatives of composite functions
```

## Usage Guide

### Commands

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
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── EXECUTION_PLAN.md      # Project specification
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── document_processor.py  # Document parsing and chunking
│   ├── vector_store.py    # Vector database (ChromaDB)
│   ├── math_tools.py      # Symbolic math (SymPy)
│   ├── tutor_engine.py    # Core tutor logic
│   └── cli.py             # Command-line interface
└── data/
    ├── documents/         # Your course materials (created automatically)
    └── vector_db/         # Vector database storage (created automatically)
```

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Document Parsing | PyMuPDF |
| Vector Database | ChromaDB |
| Embeddings | OpenAI text-embedding-3-large |
| LLM | OpenAI GPT-4o-mini |
| Symbolic Math | SymPy |
| Text Processing | LangChain, tiktoken |

## Configuration

Edit `.env` to customize settings:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here

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

## Troubleshooting

**Error: "OPENAI_API_KEY not set"**
- Make sure you've created a `.env` file with your API key

**No relevant materials found**
- Ensure you've ingested documents using the `ingest` command
- Check that your question relates to the ingested materials

**Import errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment

## Future Enhancements

Potential additions:
- Web interface (Streamlit/Gradio)
- Support for more document formats
- Image/diagram recognition (OCR)
- LaTeX rendering for math expressions
- Export conversation history
- Multiple user profiles
- Spaced repetition for practice problems

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to fork, modify, and submit pull requests!

---

**Happy Learning! 🎓📚**

