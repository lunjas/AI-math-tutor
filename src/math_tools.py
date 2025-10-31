"""Mathematical computation tools using SymPy."""

import sympy as sp
from sympy import symbols, simplify, expand, factor, solve, diff, integrate, latex
from typing import Dict, Any, Optional


class MathTools:
    """Provides symbolic math computation capabilities."""
    
    @staticmethod
    def simplify_expression(expression: str) -> Dict[str, Any]:
        """Simplify a mathematical expression.
        
        Args:
            expression: Mathematical expression as string
            
        Returns:
            Dictionary with result and LaTeX representation
        """
        try:
            expr = sp.sympify(expression)
            result = simplify(expr)
            return {
                'success': True,
                'original': str(expr),
                'result': str(result),
                'latex': latex(result)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def solve_equation(equation: str, variable: str = 'x') -> Dict[str, Any]:
        """Solve an equation.
        
        Args:
            equation: Equation as string (e.g., "x**2 - 4 = 0")
            variable: Variable to solve for
            
        Returns:
            Dictionary with solutions
        """
        try:
            var = symbols(variable)
            # Parse equation (assume format: "left = right" or just "expression")
            if '=' in equation:
                left, right = equation.split('=')
                expr = sp.sympify(left) - sp.sympify(right)
            else:
                expr = sp.sympify(equation)
            
            solutions = solve(expr, var)
            return {
                'success': True,
                'variable': variable,
                'solutions': [str(sol) for sol in solutions],
                'solutions_latex': [latex(sol) for sol in solutions]
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def derivative(expression: str, variable: str = 'x', order: int = 1) -> Dict[str, Any]:
        """Compute the derivative of an expression.
        
        Args:
            expression: Expression as string
            variable: Variable to differentiate with respect to
            order: Order of derivative
            
        Returns:
            Dictionary with derivative result
        """
        try:
            var = symbols(variable)
            expr = sp.sympify(expression)
            result = diff(expr, var, order)
            return {
                'success': True,
                'original': str(expr),
                'derivative': str(result),
                'latex': latex(result),
                'order': order,
                'variable': variable
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def integral(expression: str, variable: str = 'x', 
                 lower_bound: Optional[str] = None, 
                 upper_bound: Optional[str] = None) -> Dict[str, Any]:
        """Compute the integral of an expression.
        
        Args:
            expression: Expression as string
            variable: Variable to integrate with respect to
            lower_bound: Lower bound for definite integral (optional)
            upper_bound: Upper bound for definite integral (optional)
            
        Returns:
            Dictionary with integral result
        """
        try:
            var = symbols(variable)
            expr = sp.sympify(expression)
            
            if lower_bound is not None and upper_bound is not None:
                # Definite integral
                lb = sp.sympify(lower_bound)
                ub = sp.sympify(upper_bound)
                result = integrate(expr, (var, lb, ub))
                integral_type = 'definite'
            else:
                # Indefinite integral
                result = integrate(expr, var)
                integral_type = 'indefinite'
            
            return {
                'success': True,
                'original': str(expr),
                'integral': str(result),
                'latex': latex(result),
                'type': integral_type,
                'variable': variable
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def expand_expression(expression: str) -> Dict[str, Any]:
        """Expand a mathematical expression.
        
        Args:
            expression: Expression as string
            
        Returns:
            Dictionary with expanded result
        """
        try:
            expr = sp.sympify(expression)
            result = expand(expr)
            return {
                'success': True,
                'original': str(expr),
                'expanded': str(result),
                'latex': latex(result)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def factor_expression(expression: str) -> Dict[str, Any]:
        """Factor a mathematical expression.
        
        Args:
            expression: Expression as string
            
        Returns:
            Dictionary with factored result
        """
        try:
            expr = sp.sympify(expression)
            result = factor(expr)
            return {
                'success': True,
                'original': str(expr),
                'factored': str(result),
                'latex': latex(result)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

