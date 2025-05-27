"""
Dataset models
"""

from sqlalchemy import Column, Integer, String, Boolean, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class Dataset(Base, TimestampMixin):
    """Dataset model for storing dataset information"""
    
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    blockchain_id = Column(Integer, unique=True, index=True, nullable=True)  # ID from smart contract
    
    # Basic information
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)  # Array of tags
    
    # File information
    filename = Column(String(255), nullable=False)
    file_type = Column(String(10), nullable=False)
    file_size = Column(Integer, nullable=False)  # Size in bytes
    ipfs_hash = Column(String(100), nullable=False, index=True)
    
    # Pricing and access
    price = Column(Float, nullable=False)  # Price in STX
    is_free = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Metadata
    records_count = Column(Integer, nullable=False)
    columns_count = Column(Integer, nullable=False)
    metadata = Column(JSON, nullable=True)  # Detailed metadata
    preview_data = Column(JSON, nullable=True)  # Sample data for preview
    
    # Quality and ratings
    quality_score = Column(Float, default=0.0, nullable=False)
    average_rating = Column(Float, default=0.0, nullable=False)
    rating_count = Column(Integer, default=0, nullable=False)
    
    # Sales statistics
    total_sales = Column(Integer, default=0, nullable=False)
    total_revenue = Column(Float, default=0.0, nullable=False)
    
    # Owner relationship
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="datasets")
    
    # Access and ratings relationships
    access_records = relationship("DatasetAccess", back_populates="dataset")
    ratings = relationship("DatasetRating", back_populates="dataset")
    
    def __repr__(self):
        return f"<Dataset(id={self.id}, title='{self.title}', price={self.price})>"


class DatasetAccess(Base, TimestampMixin):
    """Model for tracking dataset access/purchases"""
    
    __tablename__ = "dataset_access"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # References
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Purchase information
    transaction_hash = Column(String(100), nullable=True)  # Blockchain transaction hash
    price_paid = Column(Float, nullable=False)  # Price paid in STX
    
    # Access control
    access_granted = Column(Boolean, default=True, nullable=False)
    download_count = Column(Integer, default=0, nullable=False)
    last_accessed = Column(TimestampMixin.created_at, nullable=True)
    
    # Relationships
    dataset = relationship("Dataset", back_populates="access_records")
    user = relationship("User", back_populates="purchases")
    
    def __repr__(self):
        return f"<DatasetAccess(dataset_id={self.dataset_id}, user_id={self.user_id})>"


class DatasetRating(Base, TimestampMixin):
    """Model for dataset ratings and reviews"""
    
    __tablename__ = "dataset_ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # References
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Rating information
    rating = Column(Integer, nullable=False)  # 1-5 stars
    review = Column(Text, nullable=True)
    
    # Verification
    is_verified_purchase = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    dataset = relationship("Dataset", back_populates="ratings")
    user = relationship("User", back_populates="ratings_given")
    
    def __repr__(self):
        return f"<DatasetRating(dataset_id={self.dataset_id}, rating={self.rating})>"
