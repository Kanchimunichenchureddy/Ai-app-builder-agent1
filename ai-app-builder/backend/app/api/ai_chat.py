from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import json

from ..core.database import get_db
from ..core.security import verify_token
from ..models.user import User
from ..services.ai_agent import AIAgentService

router = APIRouter()
security = HTTPBearer()
ai_agent = AIAgentService()

async def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)) -> User:
    """Get current authenticated user."""
    payload = verify_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.post("/chat")
async def chat_with_ai(
    chat_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with AI assistant for application building.
    """
    try:
        message = chat_data.get("message", "")
        context = chat_data.get("context", {})
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message is required"
            )
        
        # Use AI agent to generate response
        response = await ai_agent.chat_with_user(message, context)
        
        return {
            "success": True,
            "response": response,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )

@router.post("/generate-code")
async def generate_code_from_description(
    code_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate code based on natural language description.
    """
    try:
        request = code_data.get("request", "")
        context = code_data.get("context", {})
        
        if not request:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request description is required"
            )
        
        # Use AI agent to generate code
        generated_code = await ai_agent.generate_code_from_description(request, context)
        
        return {
            "success": True,
            "code": generated_code,
            "language": context.get("language", "javascript"),
            "message": "Code successfully generated"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code generation failed: {str(e)}"
        )

@router.post("/suggest-next")
async def suggest_next_steps(
    suggestion_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI suggestions for next steps in application development.
    """
    try:
        context = suggestion_data.get("context", {})
        history = suggestion_data.get("history", [])
        
        # Use AI agent to suggest next steps
        suggestions = await ai_agent.suggest_next_steps(context, history)
        
        return {
            "success": True,
            "suggestions": suggestions,
            "message": "Next steps suggested"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Suggestion failed: {str(e)}"
        )

@router.post("/explain")
async def explain_concept(
    explanation_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI explanation for code or concepts.
    """
    try:
        concept = explanation_data.get("concept", "")
        context = explanation_data.get("context", {})
        
        if not concept:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Concept to explain is required"
            )
        
        # Use AI agent to explain concept
        explanation = await ai_agent.explain_concept(concept, context)
        
        return {
            "success": True,
            "explanation": explanation,
            "message": "Concept explained"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Explanation failed: {str(e)}"
        )

@router.post("/debug")
async def debug_code(
    debug_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Debug code issues with AI assistance.
    """
    try:
        code = debug_data.get("code", "")
        error = debug_data.get("error", "")
        context = debug_data.get("context", {})
        
        if not code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code to debug is required"
            )
        
        # Use AI agent to debug code
        debug_result = await ai_agent.debug_code(code, error, context)
        
        return {
            "success": True,
            "debug_result": debug_result,
            "message": "Code debugged successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Debug failed: {str(e)}"
        )

@router.post("/optimize")
async def optimize_code(
    optimization_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Optimize code with AI assistance.
    """
    try:
        code = optimization_data.get("code", "")
        context = optimization_data.get("context", {})
        
        if not code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code to optimize is required"
            )
        
        # Use AI agent to optimize code
        optimization_result = await ai_agent.optimize_code(code, context)
        
        return {
            "success": True,
            "optimized_code": optimization_result.get("optimized_code", ""),
            "improvements": optimization_result.get("improvements", []),
            "message": "Code optimized successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Optimization failed: {str(e)}"
        )