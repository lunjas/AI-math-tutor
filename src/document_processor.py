"""Document processing module for ingesting course materials."""

import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict
import tiktoken
from src.config import Config


class DocumentProcessor:
    """Handles document parsing and chunking."""
    
    def __init__(self):
        self.config = Config()
        self.encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    
    def load_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        doc = fitz.open(pdf_path)
        text = ""
        for page_num, page in enumerate(doc):
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.get_text()
        doc.close()
        return text
    
    def load_text_file(self, file_path: str) -> str:
        """Load content from a text file.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            File content
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_document(self, file_path: str) -> str:
        """Load a document based on its file type.
        
        Args:
            file_path: Path to the document
            
        Returns:
            Document content as text
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() == '.pdf':
            return self.load_pdf(file_path)
        elif path.suffix.lower() in ['.txt', '.md']:
            return self.load_text_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")
    
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
        """
        return len(self.encoding.encode(text))
    
    def chunk_text(self, text: str, source: str) -> List[Dict[str, any]]:
        """Chunk text into smaller segments for embedding.
        
        Args:
            text: Text to chunk
            source: Source file name
            
        Returns:
            List of chunks with metadata
        """
        chunks = []
        chunk_size = self.config.CHUNK_SIZE
        chunk_overlap = self.config.CHUNK_OVERLAP
        
        # Split by paragraphs first for better semantic boundaries
        paragraphs = text.split('\n\n')
        
        current_chunk = ""
        chunk_id = 0
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # If adding this paragraph exceeds chunk size, save current chunk
            if current_chunk and self.count_tokens(current_chunk + "\n\n" + paragraph) > chunk_size:
                chunks.append({
                    'id': f"{source}_chunk_{chunk_id}",
                    'text': current_chunk.strip(),
                    'source': source,
                    'chunk_id': chunk_id,
                    'token_count': self.count_tokens(current_chunk)
                })
                chunk_id += 1
                
                # Keep overlap from the end of the previous chunk
                tokens = self.encoding.encode(current_chunk)
                if len(tokens) > chunk_overlap:
                    overlap_tokens = tokens[-chunk_overlap:]
                    current_chunk = self.encoding.decode(overlap_tokens) + "\n\n" + paragraph
                else:
                    current_chunk = paragraph
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append({
                'id': f"{source}_chunk_{chunk_id}",
                'text': current_chunk.strip(),
                'source': source,
                'chunk_id': chunk_id,
                'token_count': self.count_tokens(current_chunk)
            })
        
        return chunks
    
    def process_document(self, file_path: str) -> List[Dict[str, any]]:
        """Process a document: load and chunk it.
        
        Args:
            file_path: Path to the document
            
        Returns:
            List of chunks with metadata
        """
        source = Path(file_path).name
        text = self.load_document(file_path)
        chunks = self.chunk_text(text, source)
        
        print(f"Processed '{source}': {len(chunks)} chunks created")
        return chunks

