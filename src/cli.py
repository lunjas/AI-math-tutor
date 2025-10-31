"""Command-line interface for the AI Math Tutor."""

import sys
from pathlib import Path
from src.config import Config
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from src.tutor_engine import TutorEngine


class MathTutorCLI:
    """Command-line interface for interacting with the tutor."""
    
    def __init__(self):
        self.config = Config()
        self.doc_processor = DocumentProcessor()
        self.vector_store = VectorStore()
        self.tutor = TutorEngine(self.vector_store)
        
    def print_welcome(self):
        """Print welcome message."""
        print("\n" + "="*60)
        print("🎓 AI Math Tutor - Your Personal Learning Assistant")
        print("="*60)
        print("\nAvailable commands:")
        print("  ask <question>     - Ask the tutor a question")
        print("  compute <expr>     - Perform symbolic math computation")
        print("  quiz <topic>       - Generate practice problems")
        print("  ingest <file>      - Add a document to the knowledge base")
        print("  stats              - View knowledge base statistics")
        print("  clear              - Clear conversation history")
        print("  help               - Show this help message")
        print("  exit               - Exit the tutor")
        print("\nType 'help' anytime to see these commands again.")
        print("="*60 + "\n")
    
    def print_help(self):
        """Print detailed help."""
        print("\n" + "="*60)
        print("HELP - AI Math Tutor Commands")
        print("="*60)
        print("\n1. ASK QUESTIONS")
        print("   ask <your question>")
        print("   Example: ask What is the derivative of x^2?")
        print("   Example: ask Explain the chain rule")
        
        print("\n2. SYMBOLIC COMPUTATION")
        print("   compute <operation> <expression>")
        print("   Operations: simplify, solve, derivative, integral, expand, factor")
        print("   Example: compute simplify (x+1)*(x-1)")
        print("   Example: compute solve x**2 - 4 = 0")
        print("   Example: compute derivative x**3 + 2*x")
        
        print("\n3. GENERATE QUIZ")
        print("   quiz <topic> [number]")
        print("   Example: quiz derivatives")
        print("   Example: quiz integration 5")
        
        print("\n4. INGEST DOCUMENTS")
        print("   ingest <filepath>")
        print("   Supported: PDF, TXT, MD files")
        print("   Example: ingest ~/Documents/calc_notes.pdf")
        
        print("\n5. OTHER COMMANDS")
        print("   stats  - View knowledge base statistics")
        print("   clear  - Clear conversation history")
        print("   exit   - Exit the application")
        print("="*60 + "\n")
    
    def handle_ask(self, question: str):
        """Handle ask command."""
        if not question.strip():
            print("❌ Please provide a question.")
            return
        
        print("\n🤔 Thinking...\n")
        response = self.tutor.ask(question)
        print(f"🎓 Tutor: {response}\n")
    
    def handle_compute(self, args: str):
        """Handle compute command."""
        parts = args.strip().split(maxsplit=1)
        if len(parts) < 2:
            print("❌ Usage: compute <operation> <expression>")
            print("   Operations: simplify, solve, derivative, integral, expand, factor")
            return
        
        operation, expression = parts
        operation = operation.lower()
        
        valid_ops = ['simplify', 'solve', 'derivative', 'integral', 'expand', 'factor']
        if operation not in valid_ops:
            print(f"❌ Invalid operation. Choose from: {', '.join(valid_ops)}")
            return
        
        print("\n🔢 Computing...\n")
        result = self.tutor.compute(expression, operation)
        print(result)
    
    def handle_quiz(self, args: str):
        """Handle quiz command."""
        parts = args.strip().split()
        if not parts:
            print("❌ Please provide a topic.")
            return
        
        topic = parts[0]
        num_questions = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 3
        
        print(f"\n📝 Generating {num_questions} practice problems on '{topic}'...\n")
        quiz = self.tutor.create_quiz(topic, num_questions)
        print(quiz)
        print("\n")
    
    def handle_ingest(self, filepath: str):
        """Handle ingest command."""
        filepath = filepath.strip()
        if not filepath:
            print("❌ Please provide a file path.")
            return
        
        # Expand user path
        path = Path(filepath).expanduser()
        
        if not path.exists():
            print(f"❌ File not found: {filepath}")
            return
        
        try:
            print(f"\n📄 Processing document: {path.name}...")
            chunks = self.doc_processor.process_document(str(path))
            self.vector_store.add_chunks(chunks)
            print(f"✅ Successfully ingested '{path.name}'\n")
        except Exception as e:
            print(f"❌ Error processing document: {e}\n")
    
    def handle_stats(self):
        """Handle stats command."""
        stats = self.vector_store.get_collection_stats()
        print("\n" + "="*40)
        print("📊 Knowledge Base Statistics")
        print("="*40)
        print(f"Total chunks: {stats['total_chunks']}")
        print(f"Collection: {stats['collection_name']}")
        print("="*40 + "\n")
    
    def handle_clear(self):
        """Handle clear command."""
        self.tutor.clear_history()
        print("✅ Conversation history cleared.\n")
    
    def process_command(self, user_input: str) -> bool:
        """Process a user command.
        
        Args:
            user_input: User input string
            
        Returns:
            True to continue, False to exit
        """
        user_input = user_input.strip()
        
        if not user_input:
            return True
        
        # Parse command
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Goodbye! Happy learning!\n")
            return False
        
        elif user_input.lower() == 'help':
            self.print_help()
        
        elif user_input.startswith('ask '):
            question = user_input[4:]
            self.handle_ask(question)
        
        elif user_input.startswith('compute '):
            args = user_input[8:]
            self.handle_compute(args)
        
        elif user_input.startswith('quiz '):
            args = user_input[5:]
            self.handle_quiz(args)
        
        elif user_input.startswith('ingest '):
            filepath = user_input[7:]
            self.handle_ingest(filepath)
        
        elif user_input.lower() == 'stats':
            self.handle_stats()
        
        elif user_input.lower() == 'clear':
            self.handle_clear()
        
        else:
            # Default to asking a question
            self.handle_ask(user_input)
        
        return True
    
    def run(self):
        """Run the CLI main loop."""
        self.print_welcome()
        
        while True:
            try:
                user_input = input("📚 You: ")
                should_continue = self.process_command(user_input)
                if not should_continue:
                    break
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Happy learning!\n")
                break
            except EOFError:
                print("\n\n👋 Goodbye! Happy learning!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
                continue

