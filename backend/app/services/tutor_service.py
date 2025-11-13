"""Enhanced tutor service with streaming support."""

import sys
from pathlib import Path
from typing import AsyncGenerator, Optional, Dict, Any, List
import asyncio

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.tutor_engine import TutorEngine
from src.vector_store import VectorStore
from src.math_tools import MathTools
from src.document_processor import DocumentProcessor
from backend.app.config import settings
from backend.app.utils.logger import setup_logger

logger = setup_logger(__name__)


class TutorService:
    """Enhanced tutor service with async and streaming support."""
    
    def __init__(self):
        """Initialize the tutor service."""
        try:
            settings.ensure_directories()
            self.vector_store = VectorStore()
            self.tutor_engine = TutorEngine(self.vector_store)
            self.math_tools = MathTools()
            self.document_processor = DocumentProcessor()
            logger.info("TutorService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TutorService: {e}")
            raise
    
    async def ask_async(
        self, 
        query: str, 
        use_retrieval: bool = True,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Async version of ask method.
        
        Args:
            query: User question
            use_retrieval: Whether to use RAG retrieval
            conversation_history: Optional conversation history to use
            
        Returns:
            Tutor's response
        """
        # Run the synchronous method in a thread pool
        loop = asyncio.get_event_loop()
        
        # Temporarily set conversation history if provided
        original_history = None
        if conversation_history is not None:
            original_history = self.tutor_engine.conversation_history
            self.tutor_engine.conversation_history = conversation_history
        
        try:
            response = await loop.run_in_executor(
                None,
                self.tutor_engine.ask,
                query,
                use_retrieval
            )
            return response
        finally:
            # Restore original history if we modified it
            if original_history is not None:
                self.tutor_engine.conversation_history = original_history
    
    async def ask_stream(
        self,
        query: str,
        use_retrieval: bool = True,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> AsyncGenerator[str, None]:
        """Stream the response from the tutor.
        
        Args:
            query: User question
            use_retrieval: Whether to use RAG retrieval
            conversation_history: Optional conversation history to use
            
        Yields:
            Chunks of the response
        """
        # Retrieve relevant context if enabled
        context = ""
        if use_retrieval:
            results = self.vector_store.query(query)
            if results and results["documents"] and results["documents"][0]:
                retrieved_chunks = results["documents"][0]
                context = self.tutor_engine._build_context(query, retrieved_chunks)
        
        # Build the prompt
        system_prompt, user_prompt = self.tutor_engine._create_tutor_prompt(query, context)
        
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Use provided conversation history or the engine's history
        history = conversation_history if conversation_history is not None else self.tutor_engine.conversation_history
        
        # Include recent conversation history for context
        for msg in history[-4:]:  # Last 4 messages
            messages.append(msg)
        
        messages.append({"role": "user", "content": user_prompt})
        
        # Stream the response
        full_response = ""
        try:
            stream = self.tutor_engine.client.chat.completions.create(
                model=self.tutor_engine.config.LLM_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            # Update conversation history after streaming is complete
            if conversation_history is None:
                self.tutor_engine.conversation_history.append({"role": "user", "content": query})
                self.tutor_engine.conversation_history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            logger.error(f"Error during streaming: {e}")
            yield f"\n\nError: {str(e)}"
    
    async def compute_async(
        self,
        expression: str,
        operation: str = "simplify",
        **kwargs
    ) -> Dict[str, Any]:
        """Async version of compute method.
        
        Args:
            expression: Mathematical expression
            operation: Type of operation
            **kwargs: Additional arguments
            
        Returns:
            Computation result
        """
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self.tutor_engine.compute,
            expression,
            operation,
            **kwargs
        )
        
        # Parse the string result back into a dict
        # The compute method returns a formatted string, but we need the raw result
        if operation == "simplify":
            raw_result = self.math_tools.simplify_expression(expression)
        elif operation == "solve":
            variable = kwargs.get("variable", "x")
            raw_result = self.math_tools.solve_equation(expression, variable)
        elif operation == "derivative":
            variable = kwargs.get("variable", "x")
            order = kwargs.get("order", 1)
            raw_result = self.math_tools.derivative(expression, variable, order)
        elif operation == "integral":
            variable = kwargs.get("variable", "x")
            lower = kwargs.get("lower_bound")
            upper = kwargs.get("upper_bound")
            raw_result = self.math_tools.integral(expression, variable, lower, upper)
        elif operation == "expand":
            raw_result = self.math_tools.expand_expression(expression)
        elif operation == "factor":
            raw_result = self.math_tools.factor_expression(expression)
        else:
            raw_result = {"success": False, "error": f"Unknown operation: {operation}"}
        
        return raw_result
    
    async def create_quiz_async(
        self,
        topic: str,
        num_questions: int = 3
    ) -> str:
        """Async version of create_quiz method.
        
        Args:
            topic: Topic for the quiz
            num_questions: Number of questions
            
        Returns:
            Generated quiz
        """
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self.tutor_engine.create_quiz,
            topic,
            num_questions
        )
        return result
    
    async def process_document_async(
        self,
        file_path: str
    ) -> Dict[str, Any]:
        """Process and ingest a document asynchronously.
        
        Args:
            file_path: Path to the document
            
        Returns:
            Processing result with chunk count
        """
        loop = asyncio.get_event_loop()
        
        # Process document
        chunks = await loop.run_in_executor(
            None,
            self.document_processor.process_document,
            file_path
        )
        
        # Add to vector store
        await loop.run_in_executor(
            None,
            self.vector_store.add_chunks,
            chunks
        )
        
        return {
            "success": True,
            "filename": Path(file_path).name,
            "chunks_created": len(chunks)
        }
    
    def get_vector_store_stats(self) -> Dict[str, Any]:
        """Get vector store statistics.
        
        Returns:
            Statistics dictionary
        """
        return self.vector_store.get_collection_stats()
    
    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.tutor_engine.clear_history()


# Global tutor service instance
tutor_service = TutorService()

