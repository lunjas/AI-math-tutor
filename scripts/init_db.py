#!/usr/bin/env python3
"""Initialize the vector database with documents."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config
from src.vector_store import VectorStore
from src.document_processor import DocumentProcessor


def main():
    """Initialize the vector database with documents from data/documents."""
    print("🚀 Initializing vector database...")
    
    try:
        # Validate configuration
        Config.validate()
        
        # Initialize components
        vector_store = VectorStore()
        document_processor = DocumentProcessor()
        
        # Get documents directory
        documents_path = Path(Config.DOCUMENTS_PATH)
        
        if not documents_path.exists():
            print(f"📁 Creating documents directory: {documents_path}")
            documents_path.mkdir(parents=True, exist_ok=True)
        
        # Find all documents
        document_files = []
        for ext in ['.pdf', '.txt', '.md']:
            document_files.extend(documents_path.glob(f'*{ext}'))
        
        if not document_files:
            print(f"⚠️  No documents found in {documents_path}")
            print("Please add PDF, TXT, or MD files to the documents directory.")
            return
        
        print(f"📚 Found {len(document_files)} document(s) to process")
        
        # Process each document
        total_chunks = 0
        for doc_file in document_files:
            print(f"\n📄 Processing: {doc_file.name}")
            try:
                chunks = document_processor.process_document(str(doc_file))
                vector_store.add_chunks(chunks)
                total_chunks += len(chunks)
                print(f"✅ Added {len(chunks)} chunks from {doc_file.name}")
            except Exception as e:
                print(f"❌ Error processing {doc_file.name}: {e}")
        
        # Get stats
        stats = vector_store.get_collection_stats()
        
        print("\n" + "="*50)
        print("✨ Database initialization complete!")
        print("="*50)
        print(f"📊 Total documents processed: {len(document_files)}")
        print(f"📊 Total chunks created: {total_chunks}")
        print(f"📊 Total chunks in database: {stats['total_chunks']}")
        print(f"📊 Collection: {stats['collection_name']}")
        print("="*50)
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file (copy from backend/env.example)")
        print("2. Set your AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

