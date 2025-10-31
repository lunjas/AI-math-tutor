"""Core tutor engine with retrieval and reasoning capabilities."""

from typing import List, Optional
import openai
from src.config import Config
from src.vector_store import VectorStore
from src.math_tools import MathTools


class TutorEngine:
    """AI Math Tutor engine combining RAG and reasoning."""

    def __init__(self, vector_store: VectorStore):
        self.config = Config()
        self.vector_store = vector_store
        self.math_tools = MathTools()
        self.client = openai.AzureOpenAI(
            api_key=self.config.AZURE_OPENAI_API_KEY,
            azure_endpoint=self.config.AZURE_OPENAI_ENDPOINT,
            api_version=self.config.AZURE_OPENAI_API_VERSION,
        )
        self.conversation_history = []

    def _build_context(self, query: str, retrieved_chunks: List[str]) -> str:
        """Build context from retrieved chunks.

        Args:
            query: User query
            retrieved_chunks: List of relevant text chunks

        Returns:
            Formatted context string
        """
        if not retrieved_chunks:
            return "No relevant course materials found for this query."

        context = "RELEVANT COURSE MATERIALS:\n\n"
        for i, chunk in enumerate(retrieved_chunks, 1):
            context += f"--- Section {i} ---\n{chunk}\n\n"

        return context

    def _create_tutor_prompt(self, query: str, context: str) -> str:
        """Create the full prompt for the LLM.

        Args:
            query: User query
            context: Retrieved context

        Returns:
            Complete prompt
        """
        system_prompt = """You are an expert Finnish math tutor. Your role is to help students learn and understand mathematical concepts deeply.

TUTORING PRINCIPLES:
1. Be patient and encouraging
2. Explain concepts step-by-step
3. Use the retrieved course materials when relevant
4. Provide hints before giving direct answers
5. Ask guiding questions to promote critical thinking
6. Use clear mathematical notation and explanations
7. Relate new concepts to previously learned material
8. Verify computations when needed

When solving problems:
- Break down complex problems into manageable steps
- Explain the reasoning behind each step
- Highlight common pitfalls and misconceptions
- Encourage the student to try solving parts themselves
- Use Finnish language when solving problems

When explaining concepts:
- Start with intuition before formal definitions
- Use examples and analogies
- Connect to real-world applications when possible
- Use Finnish language when explaining concepts
"""

        user_prompt = f"""{context}

STUDENT QUESTION:
{query}

Please provide a clear, pedagogical response that helps the student understand. If this is a computational problem, explain your approach and consider using symbolic math for accuracy."""

        return system_prompt, user_prompt

    def _should_use_math_tools(self, query: str) -> Optional[str]:
        """Determine if math tools should be used based on the query.

        Args:
            query: User query

        Returns:
            Tool name if applicable, None otherwise
        """
        query_lower = query.lower()

        if any(word in query_lower for word in ["simplify", "simplification"]):
            return "simplify"
        elif any(word in query_lower for word in ["solve", "solution", "roots"]):
            return "solve"
        elif any(
            word in query_lower for word in ["derivative", "differentiate", "diff"]
        ):
            return "derivative"
        elif any(
            word in query_lower for word in ["integral", "integrate", "antiderivative"]
        ):
            return "integral"
        elif any(word in query_lower for word in ["expand", "expansion"]):
            return "expand"
        elif any(
            word in query_lower for word in ["factor", "factorize", "factorization"]
        ):
            return "factor"

        return None

    def ask(self, query: str, use_retrieval: bool = True) -> str:
        """Process a student query and generate a response.

        Args:
            query: Student question
            use_retrieval: Whether to retrieve relevant course materials

        Returns:
            Tutor's response
        """
        # Retrieve relevant context if enabled
        context = ""
        if use_retrieval:
            results = self.vector_store.query(query)
            if results and results["documents"] and results["documents"][0]:
                retrieved_chunks = results["documents"][0]
                context = self._build_context(query, retrieved_chunks)

        # Build the prompt
        system_prompt, user_prompt = self._create_tutor_prompt(query, context)

        # Add to conversation history
        messages = [{"role": "system", "content": system_prompt}]

        # Include recent conversation history for context
        for msg in self.conversation_history[-4:]:  # Last 4 messages
            messages.append(msg)

        messages.append({"role": "user", "content": user_prompt})

        # Call LLM
        response = self.client.chat.completions.create(
            model=self.config.LLM_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
        )

        answer = response.choices[0].message.content

        # Update conversation history
        self.conversation_history.append({"role": "user", "content": query})
        self.conversation_history.append({"role": "assistant", "content": answer})

        return answer

    def compute(self, expression: str, operation: str = "simplify", **kwargs) -> str:
        """Perform a mathematical computation using SymPy.

        Args:
            expression: Mathematical expression
            operation: Type of operation (simplify, solve, derivative, integral, etc.)
            **kwargs: Additional arguments for the operation

        Returns:
            Formatted result
        """
        if operation == "simplify":
            result = self.math_tools.simplify_expression(expression)
        elif operation == "solve":
            variable = kwargs.get("variable", "x")
            result = self.math_tools.solve_equation(expression, variable)
        elif operation == "derivative":
            variable = kwargs.get("variable", "x")
            order = kwargs.get("order", 1)
            result = self.math_tools.derivative(expression, variable, order)
        elif operation == "integral":
            variable = kwargs.get("variable", "x")
            lower = kwargs.get("lower_bound")
            upper = kwargs.get("upper_bound")
            result = self.math_tools.integral(expression, variable, lower, upper)
        elif operation == "expand":
            result = self.math_tools.expand_expression(expression)
        elif operation == "factor":
            result = self.math_tools.factor_expression(expression)
        else:
            return f"Unknown operation: {operation}"

        if result["success"]:
            output = f"\n=== Mathematical Computation ===\n"
            output += f"Operation: {operation}\n"
            output += f"Input: {result.get('original', expression)}\n"

            if operation == "solve":
                output += f"Variable: {result['variable']}\n"
                output += f"Solutions: {', '.join(result['solutions'])}\n"
            elif operation == "derivative":
                output += f"Derivative: {result['derivative']}\n"
            elif operation == "integral":
                output += f"Integral ({result['type']}): {result['integral']}\n"
            else:
                result_key = "result" if "result" in result else list(result.keys())[2]
                output += f"Result: {result[result_key]}\n"

            return output
        else:
            return f"Error in computation: {result['error']}"

    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        print("Conversation history cleared")

    def create_quiz(self, topic: str, num_questions: int = 3) -> str:
        """Generate practice questions on a topic.

        Args:
            topic: Topic to create questions about
            num_questions: Number of questions to generate

        Returns:
            Generated quiz questions
        """
        prompt = f"""Generate {num_questions} practice problems on the topic: {topic}

Create problems that:
1. Start easier and gradually increase in difficulty
2. Cover different aspects of the topic
3. Are clear and well-formatted
4. Include a mix of conceptual and computational questions

Format each question clearly with numbering."""

        messages = [
            {
                "role": "system",
                "content": "You are an expert math tutor creating practice problems.",
            },
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat.completions.create(
            model=self.config.LLM_MODEL,
            messages=messages,
            temperature=0.8,
            max_tokens=1500,
        )

        return response.choices[0].message.content
