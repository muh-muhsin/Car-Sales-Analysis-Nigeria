"""
Security utilities for authentication and authorization
"""

import jwt
import logging
from typing import Optional, Dict, Any
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

logger = logging.getLogger(__name__)
security = HTTPBearer()


def verify_wallet_signature(signature: str, message: str, wallet_address: str) -> bool:
    """Verify wallet signature (placeholder implementation)"""
    # TODO: Implement actual Stacks wallet signature verification
    # This would use the Stacks SDK to verify the signature
    logger.info(f"Verifying signature for wallet: {wallet_address}")
    
    # For now, return True for development
    # In production, this should verify the actual cryptographic signature
    return True


def create_access_token(wallet_address: str) -> str:
    """Create JWT access token for wallet address"""
    try:
        payload = {
            "wallet_address": wallet_address,
            "type": "access_token"
        }
        
        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm="HS256"
        )
        
        return token
        
    except Exception as e:
        logger.error(f"Failed to create access token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create access token"
        )


def verify_token(token: str) -> Dict[str, Any]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        
        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get current authenticated user"""
    try:
        # Verify token
        payload = verify_token(credentials.credentials)
        wallet_address = payload.get("wallet_address")
        
        if not wallet_address:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Get or create user
        user = db.query(User).filter(User.wallet_address == wallet_address).first()
        
        if not user:
            # Create new user
            user = User(wallet_address=wallet_address)
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Created new user: {wallet_address}")
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Check if user is banned
        if user.is_banned:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is banned"
            )
        
        return {
            "id": user.id,
            "wallet_address": user.wallet_address,
            "username": user.username,
            "is_verified": user.is_verified,
            "reputation_score": user.reputation_score
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get current user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[Dict[str, Any]]:
    """Get current user if authenticated, otherwise return None"""
    if not credentials:
        return None
    
    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None


def require_verified_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Require user to be verified"""
    if not current_user.get("is_verified"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Verified account required"
        )
    
    return current_user


def check_dataset_access(
    dataset_id: int,
    user_id: int,
    db: Session
) -> bool:
    """Check if user has access to dataset"""
    from app.models.dataset import DatasetAccess, Dataset
    
    # Check if user owns the dataset
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if dataset and dataset.owner_id == user_id:
        return True
    
    # Check if user has purchased access
    access = db.query(DatasetAccess).filter(
        DatasetAccess.dataset_id == dataset_id,
        DatasetAccess.user_id == user_id,
        DatasetAccess.access_granted == True
    ).first()
    
    return access is not None
