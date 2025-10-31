#!/usr/bin/env python3
"""
AI Math Tutor - Main Entry Point

A personalized AI math tutor using RAG (Retrieval-Augmented Generation)
and light agent features to help students learn from their course materials.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.cli import MathTutorCLI


def main():
    """Main entry point for the AI Math Tutor."""
    try:
        # Validate configuration
        Config.validate()
        
        # Initialize and run CLI
        cli = MathTutorCLI()
        cli.run()
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file (copy from .env.example)")
        print("2. Set your OPENAI_API_KEY in the .env file")
        print("\nExample .env file:")
        print("OPENAI_API_KEY=sk-your-key-here")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Happy learning!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

