"""
User model
"""

from sqlalchemy import Column, Integer, String, Boolean, Text, Float
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """User model for storing user information"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String(50), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=True)
    
    # Profile information
    display_name = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Verification and status
    is_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_banned = Column(Boolean, default=False, nullable=False)
    
    # Reputation and stats
    reputation_score = Column(Float, default=0.0, nullable=False)
    total_uploads = Column(Integer, default=0, nullable=False)
    total_purchases = Column(Integer, default=0, nullable=False)
    total_earnings = Column(Float, default=0.0, nullable=False)
    
    # Relationships
    datasets = relationship("Dataset", back_populates="owner")
    purchases = relationship("DatasetAccess", back_populates="user")
    ratings_given = relationship("DatasetRating", foreign_keys="DatasetRating.user_id", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    
    def __repr__(self):
        return f"<User(wallet_address='{self.wallet_address}', username='{self.username}')>"
