"""
Authentication endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any
from app.core.database import get_db
from app.core.security import verify_wallet_signature, create_access_token, get_current_user
from app.models.user import User
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


class WalletAuthRequest(BaseModel):
    """Request model for wallet authentication"""
    wallet_address: str
    signature: str
    message: str


class AuthResponse(BaseModel):
    """Response model for authentication"""
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]


@router.post("/wallet", response_model=AuthResponse)
async def authenticate_wallet(
    auth_request: WalletAuthRequest,
    db: Session = Depends(get_db)
):
    """Authenticate user with wallet signature"""
    try:
        # Verify wallet signature
        is_valid = verify_wallet_signature(
            auth_request.signature,
            auth_request.message,
            auth_request.wallet_address
        )
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid wallet signature"
            )
        
        # Get or create user
        user = db.query(User).filter(User.wallet_address == auth_request.wallet_address).first()
        
        if not user:
            # Create new user
            user = User(wallet_address=auth_request.wallet_address)
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Created new user: {auth_request.wallet_address}")
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Create access token
        access_token = create_access_token(user.wallet_address)
        
        return AuthResponse(
            access_token=access_token,
            user={
                "id": user.id,
                "wallet_address": user.wallet_address,
                "username": user.username,
                "display_name": user.display_name,
                "is_verified": user.is_verified,
                "reputation_score": user.reputation_score,
                "total_uploads": user.total_uploads,
                "total_purchases": user.total_purchases
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )


@router.get("/me")
async def get_current_user_info(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    try:
        user = db.query(User).filter(User.id == current_user["id"]).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {
            "id": user.id,
            "wallet_address": user.wallet_address,
            "username": user.username,
            "email": user.email,
            "display_name": user.display_name,
            "bio": user.bio,
            "avatar_url": user.avatar_url,
            "website": user.website,
            "is_verified": user.is_verified,
            "reputation_score": user.reputation_score,
            "total_uploads": user.total_uploads,
            "total_purchases": user.total_purchases,
            "total_earnings": user.total_earnings,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )


@router.post("/logout")
async def logout(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Logout user (client-side token removal)"""
    return {"message": "Logged out successfully"}
