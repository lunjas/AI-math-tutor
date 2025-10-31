# Project Prompt: Build a Personalized AI Math Tutor with RAG and Light Agent Features

## Objective
Design and implement a **personalized AI math tutor** that uses **Retrieval-Augmented Generation (RAG)** and **light agent behavior** to help a user learn math from their own course materials.  
The tutor should explain concepts and solve problems, using both retrieved course knowledge and reasoning capabilities of an LLM.

---

## Core Goals  
1. **Create a functional tutor** that helps the user understand and practice math concepts from their own notes.  
2. **Integrate reasoning, retrieval, and interactivity** in a single, cohesive AI system.

---

## Context
- The user provides math course materials (e.g., PDFs, lecture notes, problem sets).  
- The system extracts, stores, and retrieves relevant information to answer or explain user questions.  
- The AI acts as a tutor — guiding, questioning and explaining.

---

## System Overview
The system consists of four major components:

### 1. Knowledge Ingestion (RAG Pipeline)
- Parse and process course documents (PDF, text, markdown).  
- Chunk the text semantically (e.g., 300–800 tokens per chunk).  
- Create vector embeddings using a model such as `text-embedding-3-large`.  
- Store embeddings and metadata in a **vector database** (e.g., Chroma, FAISS, or Pinecone).  

**Goal:** Enable the AI to recall relevant course sections for any user query.

---

### 2. Tutor Engine (Retrieval + Reasoning)
When the user asks a question:
1. Retrieve top-k relevant document chunks.  
2. Construct a **context-aware prompt** combining the retrieved text, the question, and tutoring instructions.  
3. Call the LLM to generate an educational, step-by-step explanation.  
4. Optionally, integrate with a **symbolic math engine** (e.g., SymPy or WolframAlpha API) for accurate computation.

**LLM tasks may include:**
- Explaining a topic  
- Providing guided hints instead of direct answers  
- Generating step-by-step problem solutions  
- Creating short quizzes or example exercises  

---

### 3. Interface
Command-line interface at this point is enough.

---

## ⚙️ Recommended Tech Stack

| Component | Recommended Tools |
|------------|-------------------|
| Document parsing | `PyMuPDF`, `LangChain DocumentLoaders` |
| Vector storage | `ChromaDB`, `FAISS`, or `Pinecone` |
| Embeddings | `text-embedding-3-large` |
| LLM | `gpt-5` or `claude-4.5` |
| Symbolic math engine | `SymPy`, `WolframAlpha API` |

---

## 🧩 System Flow Summary

[User Question]
↓
[Retriever] → Retrieve top-k relevant chunks from vector DB
↓
[Context Builder] → Combine retrieved text + question + tutoring instructions
↓
[LLM Reasoner] → Generate explanation / steps / quiz
↓
[Optional Tool Call] → Compute or verify math using SymPy/Wolfram
↓
[Response Generator] → Return clear, pedagogical answer to user