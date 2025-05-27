"""
Dataset endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import logging

from app.core.database import get_db
from app.core.security import get_current_user, get_optional_user, check_dataset_access
from app.models.dataset import Dataset, DatasetAccess, DatasetRating
from app.models.user import User
from app.services.storage import IPFSService
from app.services.data_processor import DataProcessor
from app.services.blockchain import StacksService

logger = logging.getLogger(__name__)
router = APIRouter()


class DatasetResponse(BaseModel):
    """Response model for dataset"""
    id: int
    title: str
    description: Optional[str]
    tags: Optional[List[str]]
    price: float
    records_count: int
    quality_score: float
    average_rating: float
    rating_count: int
    total_sales: int
    owner: Dict[str, Any]
    created_at: str
    preview_data: Optional[Dict[str, Any]]


class DatasetListResponse(BaseModel):
    """Response model for dataset list"""
    datasets: List[DatasetResponse]
    total: int
    page: int
    per_page: int


@router.get("/", response_model=DatasetListResponse)
async def list_datasets(
    page: int = 1,
    per_page: int = 20,
    search: Optional[str] = None,
    tags: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
    current_user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    """List datasets with filtering and pagination"""
    try:
        query = db.query(Dataset).filter(Dataset.is_active == True)
        
        # Apply filters
        if search:
            query = query.filter(
                Dataset.title.ilike(f"%{search}%") |
                Dataset.description.ilike(f"%{search}%")
            )
        
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",")]
            for tag in tag_list:
                query = query.filter(Dataset.tags.contains([tag]))
        
        if min_price is not None:
            query = query.filter(Dataset.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Dataset.price <= max_price)
        
        # Apply sorting
        if sort_order.lower() == "desc":
            query = query.order_by(getattr(Dataset, sort_by).desc())
        else:
            query = query.order_by(getattr(Dataset, sort_by).asc())
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        datasets = query.offset(offset).limit(per_page).all()
        
        # Format response
        dataset_responses = []
        for dataset in datasets:
            owner = db.query(User).filter(User.id == dataset.owner_id).first()
            
            dataset_responses.append(DatasetResponse(
                id=dataset.id,
                title=dataset.title,
                description=dataset.description,
                tags=dataset.tags or [],
                price=dataset.price,
                records_count=dataset.records_count,
                quality_score=dataset.quality_score,
                average_rating=dataset.average_rating,
                rating_count=dataset.rating_count,
                total_sales=dataset.total_sales,
                owner={
                    "id": owner.id,
                    "wallet_address": owner.wallet_address,
                    "username": owner.username,
                    "display_name": owner.display_name,
                    "is_verified": owner.is_verified,
                    "reputation_score": owner.reputation_score
                },
                created_at=dataset.created_at.isoformat(),
                preview_data=dataset.preview_data
            ))
        
        return DatasetListResponse(
            datasets=dataset_responses,
            total=total,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        logger.error(f"Failed to list datasets: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve datasets"
        )


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    """Get dataset by ID"""
    try:
        dataset = db.query(Dataset).filter(
            Dataset.id == dataset_id,
            Dataset.is_active == True
        ).first()
        
        if not dataset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dataset not found"
            )
        
        owner = db.query(User).filter(User.id == dataset.owner_id).first()
        
        return DatasetResponse(
            id=dataset.id,
            title=dataset.title,
            description=dataset.description,
            tags=dataset.tags or [],
            price=dataset.price,
            records_count=dataset.records_count,
            quality_score=dataset.quality_score,
            average_rating=dataset.average_rating,
            rating_count=dataset.rating_count,
            total_sales=dataset.total_sales,
            owner={
                "id": owner.id,
                "wallet_address": owner.wallet_address,
                "username": owner.username,
                "display_name": owner.display_name,
                "is_verified": owner.is_verified,
                "reputation_score": owner.reputation_score
            },
            created_at=dataset.created_at.isoformat(),
            preview_data=dataset.preview_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get dataset {dataset_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve dataset"
        )


@router.post("/upload")
async def upload_dataset(
    title: str = Form(...),
    description: str = Form(...),
    tags: str = Form(""),
    price: float = Form(...),
    file: UploadFile = File(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a new dataset"""
    try:
        # Read file content
        file_content = await file.read()
        
        # Process the file
        data_processor = DataProcessor()
        processed_data = await data_processor.process_upload(file_content, file.filename)
        
        # Upload to IPFS
        ipfs_service = IPFSService()
        ipfs_hash = await ipfs_service.upload_json(processed_data)
        
        if not ipfs_hash:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload file to IPFS"
            )
        
        # Create dataset record
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
        
        dataset = Dataset(
            title=title,
            description=description,
            tags=tag_list,
            filename=file.filename,
            file_type=file.filename.split(".")[-1].lower(),
            file_size=len(file_content),
            ipfs_hash=ipfs_hash,
            price=price,
            is_free=price == 0,
            records_count=processed_data["metadata"]["records_count"],
            columns_count=processed_data["metadata"]["columns_count"],
            metadata=processed_data["metadata"],
            preview_data=processed_data["preview"],
            quality_score=processed_data["quality_score"],
            owner_id=current_user["id"]
        )
        
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        
        # Update user stats
        user = db.query(User).filter(User.id == current_user["id"]).first()
        user.total_uploads += 1
        db.commit()
        
        logger.info(f"Dataset uploaded successfully: {dataset.id}")
        
        return {
            "message": "Dataset uploaded successfully",
            "dataset_id": dataset.id,
            "ipfs_hash": ipfs_hash
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to upload dataset: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload dataset"
        )
