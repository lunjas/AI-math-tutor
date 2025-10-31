"""Vector database module for storing and retrieving embeddings."""

import chromadb
from chromadb.config import Settings
from typing import List, Dict
import openai
from src.config import Config


class VectorStore:
    """Manages vector embeddings storage and retrieval using ChromaDB."""

    def __init__(self):
        self.config = Config()
        self.client = openai.AzureOpenAI(
            api_key=self.config.AZURE_OPENAI_API_KEY,
            azure_endpoint=self.config.AZURE_OPENAI_ENDPOINT,
            api_version=self.config.AZURE_OPENAI_API_VERSION,
        )

        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=self.config.VECTOR_DB_PATH,
            settings=Settings(anonymized_telemetry=False),
        )

        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="math_course_materials",
            metadata={"description": "Math course materials embeddings"},
        )

    def create_embedding(self, text: str) -> List[float]:
        """Create an embedding for a text using OpenAI's embedding model.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        response = self.client.embeddings.create(
            input=text, model=self.config.EMBEDDING_MODEL
        )
        return response.data[0].embedding

    def add_chunks(self, chunks: List[Dict[str, any]]):
        """Add document chunks to the vector store.

        Args:
            chunks: List of chunks with metadata
        """
        if not chunks:
            return

        print(f"Creating embeddings for {len(chunks)} chunks...")

        # Prepare data for batch insertion
        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for chunk in chunks:
            # Create embedding
            embedding = self.create_embedding(chunk["text"])

            ids.append(chunk["id"])
            embeddings.append(embedding)
            documents.append(chunk["text"])
            metadatas.append(
                {
                    "source": chunk["source"],
                    "chunk_id": chunk["chunk_id"],
                    "token_count": chunk["token_count"],
                }
            )

        # Add to ChromaDB
        self.collection.add(
            ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas
        )

        print(f"Added {len(chunks)} chunks to vector store")

    def query(self, query_text: str, top_k: int = None) -> Dict[str, any]:
        """Query the vector store for relevant chunks.

        Args:
            query_text: Query text
            top_k: Number of results to return (defaults to config value)

        Returns:
            Query results with documents and metadata
        """
        if top_k is None:
            top_k = self.config.TOP_K_RESULTS

        # Create embedding for query
        query_embedding = self.create_embedding(query_text)

        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k
        )

        return results

    def get_collection_stats(self) -> Dict[str, any]:
        """Get statistics about the vector store.

        Returns:
            Dictionary with collection statistics
        """
        count = self.collection.count()
        return {"total_chunks": count, "collection_name": self.collection.name}

    def clear_collection(self):
        """Clear all data from the collection."""
        self.chroma_client.delete_collection(name="math_course_materials")
        self.collection = self.chroma_client.get_or_create_collection(
            name="math_course_materials",
            metadata={"description": "Math course materials embeddings"},
        )
        print("Vector store cleared")
