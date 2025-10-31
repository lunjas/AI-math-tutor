"""Configuration management for the AI Math Tutor."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Central configuration class."""
    
    # API Keys
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
    
    # Model Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", str(BASE_DIR / "data" / "vector_db"))
    DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH", str(BASE_DIR / "data" / "documents"))
    
    # Retrieval Settings
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "600"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist."""
        Path(cls.VECTOR_DB_PATH).mkdir(parents=True, exist_ok=True)
        Path(cls.DOCUMENTS_PATH).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.AZURE_OPENAI_API_KEY:
            raise ValueError("AZURE_OPENAI_API_KEY not set in environment variables")
        if not cls.AZURE_OPENAI_ENDPOINT:
            raise ValueError("AZURE_OPENAI_ENDPOINT not set in environment variables")
        if not cls.AZURE_OPENAI_API_VERSION:
            raise ValueError("AZURE_OPENAI_API_VERSION not set in environment variables")
        cls.ensure_directories()

