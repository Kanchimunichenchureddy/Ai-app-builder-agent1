from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import List, Dict, Any
import json
from sqlalchemy.orm import Session

# Fix the import paths - use absolute imports
from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.services.ai_agent import AIAgentService

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

@router.post("/stripe/create-payment-intent")
async def create_stripe_payment_intent(
    payment_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a Stripe payment intent.
    """
    try:
        amount = payment_data.get("amount")
        currency = payment_data.get("currency", "usd")
        metadata = payment_data.get("metadata", {})
        
        if not amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount is required"
            )
        
        # Add user info to metadata
        metadata["user_id"] = current_user.id
        metadata["user_email"] = current_user.email
        
        result = await ai_agent.stripe_service.create_payment_intent(
            amount=amount,
            currency=currency,
            metadata=metadata
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Payment intent creation failed: {result['error']}"
            )
        
        return {
            "success": True,
            "payment_intent_id": result["payment_intent_id"],
            "client_secret": result["client_secret"],
            "status": result["status"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment intent creation failed: {str(e)}"
        )

@router.post("/stripe/create-customer")
async def create_stripe_customer(
    customer_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a Stripe customer.
    """
    try:
        email = customer_data.get("email", current_user.email)
        name = customer_data.get("name", current_user.username)
        metadata = customer_data.get("metadata", {})
        
        # Add user info to metadata
        metadata["user_id"] = current_user.id
        
        result = await ai_agent.stripe_service.create_customer(
            email=email,
            name=name,
            metadata=metadata
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Customer creation failed: {result['error']}"
            )
        
        return {
            "success": True,
            "customer_id": result["customer_id"],
            "email": result["email"],
            "name": result["name"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Customer creation failed: {str(e)}"
        )

@router.post("/google/create-drive-file")
async def create_google_drive_file(
    file_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a file in Google Drive.
    """
    try:
        # In a real implementation, you would get user's Google credentials from database
        # For now, we'll simulate this with mock credentials
        credentials = {
            "token": "mock_token",
            "refresh_token": "mock_refresh_token",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": ai_agent.google_service.client_id,
            "client_secret": ai_agent.google_service.client_secret,
            "scopes": ai_agent.google_service.scopes
        }
        
        file_name = file_data.get("file_name")
        content = file_data.get("content")
        mime_type = file_data.get("mime_type", "text/plain")
        
        if not file_name or not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File name and content are required"
            )
        
        result = await ai_agent.google_service.create_google_drive_file(
            credentials=credentials,
            file_name=file_name,
            content=content,
            mime_type=mime_type
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"File creation failed: {result['error']}"
            )
        
        return {
            "success": True,
            "file_id": result["file_id"],
            "file_name": result["file_name"],
            "mime_type": result["mime_type"],
            "web_view_link": result["web_view_link"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File creation failed: {str(e)}"
        )

@router.post("/google/create-sheet")
async def create_google_sheet(
    sheet_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a Google Sheet.
    """
    try:
        # In a real implementation, you would get user's Google credentials from database
        # For now, we'll simulate this with mock credentials
        credentials = {
            "token": "mock_token",
            "refresh_token": "mock_refresh_token",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": ai_agent.google_service.client_id,
            "client_secret": ai_agent.google_service.client_secret,
            "scopes": ai_agent.google_service.scopes
        }
        
        title = sheet_data.get("title")
        data = sheet_data.get("data")
        
        if not title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sheet title is required"
            )
        
        result = await ai_agent.google_service.create_google_sheet(
            credentials=credentials,
            title=title,
            data=data
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Sheet creation failed: {result['error']}"
            )
        
        return {
            "success": True,
            "spreadsheet_id": result["spreadsheet_id"],
            "title": result["title"],
            "url": result["url"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sheet creation failed: {str(e)}"
        )

@router.post("/deepseek/generate-code")
async def generate_code_with_deepseek(
    code_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate code using DeepSeek AI.
    """
    try:
        prompt = code_data.get("prompt")
        model = code_data.get("model", "deepseek-coder")
        max_tokens = code_data.get("max_tokens", 2000)
        temperature = code_data.get("temperature", 0.7)
        
        if not prompt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt is required"
            )
        
        result = await ai_agent.deepseek_service.generate_code(
            prompt=prompt,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Code generation failed: {result['error']}"
            )
        
        return {
            "success": True,
            "code": result["code"],
            "model": result["model"],
            "usage": result["usage"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code generation failed: {str(e)}"
        )

@router.post("/deepseek/explain-code")
async def explain_code_with_deepseek(
    explanation_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Explain code using DeepSeek AI.
    """
    try:
        code = explanation_data.get("code")
        explanation_request = explanation_data.get("request")
        model = explanation_data.get("model", "deepseek-chat")
        max_tokens = explanation_data.get("max_tokens", 1000)
        
        if not code or not explanation_request:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code and explanation request are required"
            )
        
        result = await ai_agent.deepseek_service.explain_code(
            code=code,
            explanation_request=explanation_request,
            model=model,
            max_tokens=max_tokens
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Code explanation failed: {result['error']}"
            )
        
        return {
            "success": True,
            "explanation": result["explanation"],
            "model": result["model"],
            "usage": result["usage"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code explanation failed: {str(e)}"
        )