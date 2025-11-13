"""Input validation utilities."""

import re
from typing import Optional


def validate_expression(expression: str) -> tuple[bool, Optional[str]]:
    """Validate a mathematical expression.
    
    Args:
        expression: Expression to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not expression or not expression.strip():
        return False, "Expression cannot be empty"
    
    # Check for potentially dangerous patterns
    dangerous_patterns = [
        r'__',  # Double underscore (Python internals)
        r'import\s',  # Import statements
        r'exec\s*\(',  # Exec function
        r'eval\s*\(',  # Eval function (though SymPy uses sympify)
        r'open\s*\(',  # File operations
        r'os\.',  # OS module access
        r'sys\.',  # Sys module access
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, expression, re.IGNORECASE):
            return False, f"Expression contains potentially unsafe pattern: {pattern}"
    
    return True, None


def validate_operation(operation: str) -> tuple[bool, Optional[str]]:
    """Validate a mathematical operation type.
    
    Args:
        operation: Operation to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_operations = {
        "simplify", "solve", "derivative", "integral", 
        "expand", "factor"
    }
    
    if operation.lower() not in valid_operations:
        return False, f"Invalid operation. Must be one of: {', '.join(valid_operations)}"
    
    return True, None


def validate_session_id(session_id: str) -> tuple[bool, Optional[str]]:
    """Validate a session ID format.
    
    Args:
        session_id: Session ID to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not session_id or not session_id.strip():
        return False, "Session ID cannot be empty"
    
    # Session IDs should be alphanumeric with hyphens (UUID format)
    if not re.match(r'^[a-zA-Z0-9\-]+$', session_id):
        return False, "Session ID must be alphanumeric with hyphens only"
    
    return True, None

