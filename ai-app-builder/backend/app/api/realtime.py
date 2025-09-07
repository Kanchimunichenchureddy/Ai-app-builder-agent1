from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Dict, Any
import json
import uuid

from ..core.database import get_db
from ..core.security import verify_token
from ..models.user import User
from ..services.realtime_creator import RealTimeProjectCreator

router = APIRouter()
security = HTTPBearer()

# Global instance of the real-time creator
realtime_creator = RealTimeProjectCreator()

async def get_current_user_ws(token: str, db: Session) -> User:
    """Get current authenticated user for WebSocket connections."""
    payload = verify_token(token)
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

@router.websocket("/ws/project-creation/{session_id}")
async def websocket_project_creation(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time project creation with live progress updates.
    
    Usage:
    1. Connect to WebSocket with session_id
    2. Send authentication token
    3. Send project creation request
    4. Receive real-time progress updates
    """
    try:
        await realtime_creator.connect_websocket(websocket, session_id)
        
        # Wait for authentication and project data
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("type") == "authenticate":
                    # Handle authentication
                    token = message.get("token")
                    if not token:
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": "Authentication token required"
                        }))
                        continue
                    
                    try:
                        # Get database session
                        db = next(get_db())
                        user = await get_current_user_ws(token, db)
                        
                        await websocket.send_text(json.dumps({
                            "type": "authenticated",
                            "user": {
                                "id": user.id,
                                "email": user.email,
                                "username": user.username
                            },
                            "message": f"👋 Welcome {user.username}! Ready to build your application."
                        }))
                        
                    except Exception as e:
                        await websocket.send_text(json.dumps({
                            "type": "auth_error",
                            "message": f"Authentication failed: {str(e)}"
                        }))
                        continue
                
                elif message.get("type") == "create_project":
                    # Handle project creation request
                    if 'user' not in locals():
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": "Please authenticate first"
                        }))
                        continue
                    
                    project_data = message.get("project_data", {})
                    project_data["user_id"] = user.id
                    
                    # Start real-time project creation
                    try:
                        await realtime_creator.create_project_realtime(
                            session_id, 
                            project_data, 
                            db
                        )
                    except Exception as e:
                        await websocket.send_text(json.dumps({
                            "type": "creation_error",
                            "message": f"Project creation failed: {str(e)}"
                        }))
                
                elif message.get("type") == "cancel_creation":
                    # Handle cancellation request
                    await realtime_creator.cancel_creation(session_id)
                    
                elif message.get("type") == "ping":
                    # Handle keep-alive ping
                    await websocket.send_text(json.dumps({
                        "type": "pong",
                        "timestamp": message.get("timestamp")
                    }))
                
                else:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": f"Unknown message type: {message.get('type')}"
                    }))
                    
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }))
            except Exception as e:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Error processing message: {str(e)}"
                }))
                
    except WebSocketDisconnect:
        await realtime_creator.disconnect_websocket(session_id)
    except Exception as e:
        print(f"WebSocket error for session {session_id}: {e}")
        await realtime_creator.disconnect_websocket(session_id)

@router.post("/realtime/create-session")
async def create_realtime_session(
    current_user: User = Depends(lambda token: get_current_user_ws(token.credentials, next(get_db()))),
    token: str = Depends(security)
):
    """
    Create a new real-time project creation session.
    Returns a session ID for WebSocket connection.
    """
    session_id = str(uuid.uuid4())
    
    return {
        "success": True,
        "session_id": session_id,
        "websocket_url": f"/api/v1/realtime/ws/project-creation/{session_id}",
        "message": "Session created. Connect to WebSocket to start real-time project creation."
    }

@router.get("/realtime/session/{session_id}/status")
async def get_session_status(
    session_id: str,
    current_user: User = Depends(lambda token: get_current_user_ws(token.credentials, next(get_db()))),
    token: str = Depends(security)
):
    """
    Get the current status of a real-time creation session.
    """
    status = realtime_creator.get_creation_status(session_id)
    
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or expired"
        )
    
    return {
        "success": True,
        "session_id": session_id,
        "status": status
    }

@router.post("/realtime/session/{session_id}/cancel")
async def cancel_realtime_session(
    session_id: str,
    current_user: User = Depends(lambda token: get_current_user_ws(token.credentials, next(get_db()))),
    token: str = Depends(security)
):
    """
    Cancel an ongoing real-time project creation session.
    """
    await realtime_creator.cancel_creation(session_id)
    
    return {
        "success": True,
        "session_id": session_id,
        "message": "Creation session cancelled successfully"
    }