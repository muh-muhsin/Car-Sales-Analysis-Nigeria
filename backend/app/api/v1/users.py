"""
User endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import logging

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.dataset import Dataset, DatasetAccess

logger = logging.getLogger(__name__)
router = APIRouter()


class UserProfileUpdate(BaseModel):
    """Request model for updating user profile"""
    username: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None


class UserResponse(BaseModel):
    """Response model for user"""
    id: int
    wallet_address: str
    username: Optional[str]
    email: Optional[str]
    display_name: Optional[str]
    bio: Optional[str]
    website: Optional[str]
    is_verified: bool
    reputation_score: float
    total_uploads: int
    total_purchases: int
    total_earnings: float
    created_at: str


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile"""
    try:
        user = db.query(User).filter(User.id == current_user["id"]).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            id=user.id,
            wallet_address=user.wallet_address,
            username=user.username,
            email=user.email,
            display_name=user.display_name,
            bio=user.bio,
            website=user.website,
            is_verified=user.is_verified,
            reputation_score=user.reputation_score,
            total_uploads=user.total_uploads,
            total_purchases=user.total_purchases,
            total_earnings=user.total_earnings,
            created_at=user.created_at.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile"
        )


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    try:
        user = db.query(User).filter(User.id == current_user["id"]).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields if provided
        update_data = profile_update.dict(exclude_unset=True)
        
        # Check username uniqueness
        if "username" in update_data and update_data["username"]:
            existing_user = db.query(User).filter(
                User.username == update_data["username"],
                User.id != user.id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Check email uniqueness
        if "email" in update_data and update_data["email"]:
            existing_user = db.query(User).filter(
                User.email == update_data["email"],
                User.id != user.id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Apply updates
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        
        return UserResponse(
            id=user.id,
            wallet_address=user.wallet_address,
            username=user.username,
            email=user.email,
            display_name=user.display_name,
            bio=user.bio,
            website=user.website,
            is_verified=user.is_verified,
            reputation_score=user.reputation_score,
            total_uploads=user.total_uploads,
            total_purchases=user.total_purchases,
            total_earnings=user.total_earnings,
            created_at=user.created_at.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )


@router.get("/me/datasets")
async def get_user_datasets(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's datasets"""
    try:
        datasets = db.query(Dataset).filter(
            Dataset.owner_id == current_user["id"],
            Dataset.is_active == True
        ).order_by(Dataset.created_at.desc()).all()
        
        return {
            "datasets": [
                {
                    "id": dataset.id,
                    "title": dataset.title,
                    "description": dataset.description,
                    "price": dataset.price,
                    "records_count": dataset.records_count,
                    "quality_score": dataset.quality_score,
                    "total_sales": dataset.total_sales,
                    "total_revenue": dataset.total_revenue,
                    "created_at": dataset.created_at.isoformat(),
                    "is_active": dataset.is_active
                }
                for dataset in datasets
            ],
            "total": len(datasets)
        }
        
    except Exception as e:
        logger.error(f"Failed to get user datasets: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user datasets"
        )


@router.get("/me/purchases")
async def get_user_purchases(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's purchases"""
    try:
        purchases = db.query(DatasetAccess).filter(
            DatasetAccess.user_id == current_user["id"],
            DatasetAccess.access_granted == True
        ).order_by(DatasetAccess.created_at.desc()).all()
        
        purchase_data = []
        for purchase in purchases:
            dataset = db.query(Dataset).filter(Dataset.id == purchase.dataset_id).first()
            if dataset:
                purchase_data.append({
                    "id": purchase.id,
                    "dataset": {
                        "id": dataset.id,
                        "title": dataset.title,
                        "description": dataset.description,
                        "records_count": dataset.records_count,
                        "quality_score": dataset.quality_score
                    },
                    "price_paid": purchase.price_paid,
                    "purchased_at": purchase.created_at.isoformat(),
                    "download_count": purchase.download_count,
                    "last_accessed": purchase.last_accessed.isoformat() if purchase.last_accessed else None
                })
        
        return {
            "purchases": purchase_data,
            "total": len(purchase_data)
        }
        
    except Exception as e:
        logger.error(f"Failed to get user purchases: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user purchases"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user by ID (public profile)"""
    try:
        user = db.query(User).filter(
            User.id == user_id,
            User.is_active == True
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Return public profile (limited information)
        return UserResponse(
            id=user.id,
            wallet_address=user.wallet_address,
            username=user.username,
            email=None,  # Don't expose email in public profile
            display_name=user.display_name,
            bio=user.bio,
            website=user.website,
            is_verified=user.is_verified,
            reputation_score=user.reputation_score,
            total_uploads=user.total_uploads,
            total_purchases=user.total_purchases,
            total_earnings=0.0,  # Don't expose earnings in public profile
            created_at=user.created_at.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )
