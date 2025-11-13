"""Enhanced configuration for FastAPI backend."""

from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    
    # Model Configuration
    EMBEDDING_MODEL: str = "text-embedding-3-large"
    LLM_MODEL: str = "gpt-4o-mini"
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    VECTOR_DB_PATH: str = str(BASE_DIR / "data" / "vector_db")
    DOCUMENTS_PATH: str = str(BASE_DIR / "data" / "documents")
    
    # Retrieval Settings
    TOP_K_RESULTS: int = 3
    CHUNK_SIZE: int = 600
    CHUNK_OVERLAP: int = 100
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = False
    
    # CORS Settings
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        Path(self.VECTOR_DB_PATH).mkdir(parents=True, exist_ok=True)
        Path(self.DOCUMENTS_PATH).mkdir(parents=True, exist_ok=True)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

