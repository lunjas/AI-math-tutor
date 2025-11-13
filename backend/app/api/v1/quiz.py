"""Quiz generation endpoints."""

from fastapi import APIRouter, HTTPException, status
from backend.app.models.quiz import QuizRequest, QuizResponse
from backend.app.services.tutor_service import tutor_service
from backend.app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    """Generate practice quiz questions on a topic.
    
    Args:
        request: Quiz request with topic and number of questions
        
    Returns:
        Generated quiz questions
    """
    try:
        # Generate quiz
        questions = await tutor_service.create_quiz_async(
            topic=request.topic,
            num_questions=request.num_questions
        )
        
        return QuizResponse(
            topic=request.topic,
            questions=questions,
            num_questions=request.num_questions
        )
        
    except Exception as e:
        logger.error(f"Error in quiz generation endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Quiz generation failed: {str(e)}"
        )

