"""Computation endpoints for mathematical operations."""

from fastapi import APIRouter, HTTPException, status
from backend.app.models.compute import ComputeRequest, ComputeResponse
from backend.app.services.tutor_service import tutor_service
from backend.app.utils.validators import validate_expression, validate_operation
from backend.app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/", response_model=ComputeResponse)
async def compute(request: ComputeRequest):
    """Perform a mathematical computation.
    
    Args:
        request: Computation request with expression and operation
        
    Returns:
        Computation result
    """
    try:
        # Validate expression
        is_valid, error_msg = validate_expression(request.expression)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        # Validate operation
        is_valid, error_msg = validate_operation(request.operation)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        # Prepare kwargs for the computation
        kwargs = {}
        if request.variable:
            kwargs["variable"] = request.variable
        if request.order:
            kwargs["order"] = request.order
        if request.lower_bound:
            kwargs["lower_bound"] = request.lower_bound
        if request.upper_bound:
            kwargs["upper_bound"] = request.upper_bound
        
        # Perform computation
        result = await tutor_service.compute_async(
            expression=request.expression,
            operation=request.operation,
            **kwargs
        )
        
        # Build response
        response_data = {
            "success": result.get("success", False),
            "operation": request.operation,
            "original": result.get("original", request.expression),
            "error": result.get("error")
        }
        
        # Add operation-specific fields
        if result.get("success"):
            if request.operation == "solve":
                response_data["result"] = ", ".join(result.get("solutions", []))
                response_data["details"] = {
                    "solutions": result.get("solutions", []),
                    "variable": result.get("variable")
                }
            elif request.operation == "derivative":
                response_data["result"] = result.get("derivative")
                response_data["latex"] = result.get("latex")
                response_data["details"] = {
                    "order": result.get("order"),
                    "variable": result.get("variable")
                }
            elif request.operation == "integral":
                response_data["result"] = result.get("integral")
                response_data["latex"] = result.get("latex")
                response_data["details"] = {
                    "type": result.get("type"),
                    "variable": result.get("variable")
                }
            elif request.operation == "simplify":
                response_data["result"] = result.get("result")
                response_data["latex"] = result.get("latex")
            elif request.operation == "expand":
                response_data["result"] = result.get("expanded")
                response_data["latex"] = result.get("latex")
            elif request.operation == "factor":
                response_data["result"] = result.get("factored")
                response_data["latex"] = result.get("latex")
        
        return ComputeResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in compute endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Computation failed: {str(e)}"
        )

