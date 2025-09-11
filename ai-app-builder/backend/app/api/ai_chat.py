from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.services.ai_agent import AIAgentService
from app.api.auth import oauth2_scheme
from app.core.security import verify_token

router = APIRouter()
ai_agent = AIAgentService()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Get current user from token."""
    try:
        payload = verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/chat")
async def chat_with_user(
    message_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with AI assistant.
    """
    try:
        message = message_data.get("message", "")
        context = message_data.get("context", {})
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message is required"
            )
        
        # Add user ID to context
        context["user_id"] = str(current_user.id)
        
        # Use AI agent to generate response
        response = await ai_agent.chat_with_user(message, context)
        
        return {
            "success": True,
            "response": response,
            "message": "Response generated"
        }
        
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service connection failed: {e}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )

@router.post("/explain")
async def explain_concept(
    explanation_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Explain programming concepts with AI assistance.
    """
    try:
        concept = explanation_data.get("concept", "")
        context = explanation_data.get("context", {})
        
        if not concept:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Concept to explain is required"
            )
        
        # Add user ID to context
        context["user_id"] = str(current_user.id)
        
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
        
        # Add user ID to context
        context["user_id"] = str(current_user.id)
        
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
        
        # Add user ID to context
        context["user_id"] = str(current_user.id)
        
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

@router.post("/security-review")
async def security_review(
    review_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Review code for security vulnerabilities.
    """
    try:
        code = review_data.get("code", "")
        context = review_data.get("context", {})
        
        if not code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code to review is required"
            )
        
        # Add user ID to context
        context["user_id"] = str(current_user.id)
        
        # Use AI agent to review code security
        security_review_result = await ai_agent.review_code_security(code, context)
        
        return {
            "success": True,
            "security_review": security_review_result.get("review", ""),
            "vulnerabilities": security_review_result.get("vulnerabilities_found", []),
            "message": "Security review completed"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Security review failed: {str(e)}"
        )

@router.post("/architecture-analysis")
async def architecture_analysis(
    analysis_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze project architecture.
    """
    try:
        project_description = analysis_data.get("description", "")
        tech_stack = analysis_data.get("tech_stack", {})
        
        if not project_description:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project description is required"
            )
        
        # Add user ID to context
        context = {"user_id": str(current_user.id)}
        
        # Use AI agent to analyze architecture
        architecture_result = await ai_agent.analyze_project_architecture(project_description, tech_stack)
        
        return {
            "success": True,
            "architecture_analysis": architecture_result.get("analysis", ""),
            "message": "Architecture analysis completed"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Architecture analysis failed: {str(e)}"
        )

@router.post("/generate-documentation")
async def generate_documentation(
    doc_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate project documentation.
    """
    try:
        project_data = doc_data.get("project_data", {})
        
        # Add user ID to context
        context = {"user_id": str(current_user.id)}
        
        # Use AI agent to generate documentation
        documentation = await ai_agent.generate_documentation(project_data)
        
        return {
            "success": True,
            "documentation": documentation,
            "message": "Documentation generated"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Documentation generation failed: {str(e)}"
        )

@router.post("/suggest-improvements")
async def suggest_improvements(
    improvement_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Suggest improvements for a project.
    """
    try:
        project_data = improvement_data.get("project_data", {})
        feedback = improvement_data.get("feedback", "")
        
        # Add user ID to context
        context = {"user_id": str(current_user.id)}
        
        # Use AI agent to suggest improvements
        suggestions_result = await ai_agent.suggest_improvements(project_data, feedback)
        
        return {
            "success": True,
            "suggestions": suggestions_result.get("suggestions", ""),
            "message": "Improvement suggestions generated"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Improvement suggestions failed: {str(e)}"
        )