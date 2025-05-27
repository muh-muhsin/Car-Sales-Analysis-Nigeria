"""
Transaction model
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum


class TransactionType(enum.Enum):
    """Transaction types"""
    DATASET_PURCHASE = "dataset_purchase"
    DATASET_SALE = "dataset_sale"
    PLATFORM_FEE = "platform_fee"
    WITHDRAWAL = "withdrawal"


class TransactionStatus(enum.Enum):
    """Transaction status"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Transaction(Base, TimestampMixin):
    """Transaction model for tracking all financial transactions"""
    
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Blockchain information
    transaction_hash = Column(String(100), unique=True, index=True, nullable=False)
    block_height = Column(Integer, nullable=True)
    
    # Transaction details
    transaction_type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING, nullable=False)
    
    # Financial information
    amount = Column(Float, nullable=False)  # Amount in STX
    fee = Column(Float, default=0.0, nullable=False)  # Transaction fee
    platform_fee = Column(Float, default=0.0, nullable=False)  # Platform fee (5%)
    
    # References
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=True)  # Null for non-dataset transactions
    
    # Additional metadata
    metadata = Column(String(500), nullable=True)  # JSON string for additional data
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(hash='{self.transaction_hash}', type='{self.transaction_type}', amount={self.amount})>"
