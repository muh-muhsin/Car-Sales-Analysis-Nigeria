"""
Cars360 Backend API
Main FastAPI application for the decentralized car sales data marketplace
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse, StreamingResponse
from contextlib import asynccontextmanager
import uvicorn
import os
from typing import List, Optional, Dict, Any
import pandas as pd
import json
from datetime import datetime
import logging

from app.core.config import settings
from app.core.database import engine, SessionLocal, init_db
from app.core.security import verify_wallet_signature, get_current_user
from app.api.v1 import datasets, users, analytics, auth
from app.models import Base
from app.services.blockchain import StacksService
from app.services.storage import IPFSService
from app.services.data_processor import DataProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Cars360 API...")

    # Initialize database
    Base.metadata.create_all(bind=engine)

    # Initialize services
    app.state.stacks_service = StacksService()
    app.state.ipfs_service = IPFSService()
    app.state.data_processor = DataProcessor()

    logger.info("Cars360 API started successfully")

    yield

    # Shutdown
    logger.info("Shutting down Cars360 API...")

# Create FastAPI app
app = FastAPI(
    title="Cars360 API",
    description="Decentralized car sales data marketplace API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(datasets.router, prefix="/api/v1/datasets", tags=["Datasets"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Cars360 API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()

        # Check blockchain connection
        stacks_service = app.state.stacks_service
        blockchain_status = await stacks_service.get_network_status()

        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "database": "connected",
                "blockchain": "connected" if blockchain_status else "disconnected",
                "ipfs": "connected"  # TODO: Add IPFS health check
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/api/v1/stats")
async def get_marketplace_stats():
    """Get marketplace statistics"""
    try:
        stacks_service = app.state.stacks_service
        stats = await stacks_service.get_marketplace_stats()

        # Add additional stats from database
        db = SessionLocal()
        try:
            # TODO: Add database queries for additional stats
            additional_stats = {
                "total_users": 0,  # Query from database
                "active_datasets": 0,  # Query from database
                "recent_transactions": 0  # Query from database
            }

            return {
                **stats,
                **additional_stats,
                "last_updated": datetime.utcnow().isoformat()
            }
        finally:
            db.close()

    except Exception as e:
        logger.error(f"Failed to get marketplace stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")

@app.post("/api/v1/datasets/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    price: int = Form(...),
    tags: str = Form(""),
    current_user: dict = Depends(get_current_user)
):
    """Upload a new dataset"""
    try:
        # Validate file type
        if not file.filename.endswith(('.csv', '.xlsx', '.json')):
            raise HTTPException(
                status_code=400,
                detail="Only CSV, XLSX, and JSON files are supported"
            )

        # Process and validate data
        data_processor = app.state.data_processor
        processed_data = await data_processor.process_upload(file)

        # Upload to IPFS
        ipfs_service = app.state.ipfs_service
        ipfs_hash = await ipfs_service.upload_file(processed_data)

        # Create metadata
        metadata = {
            "title": title,
            "description": description,
            "tags": tags.split(",") if tags else [],
            "file_type": file.filename.split(".")[-1],
            "upload_date": datetime.utcnow().isoformat(),
            "records_count": len(processed_data),
            "ipfs_hash": ipfs_hash
        }

        # Register on blockchain
        stacks_service = app.state.stacks_service
        dataset_id = await stacks_service.register_dataset(
            uri=f"ipfs://{ipfs_hash}",
            price=price,
            metadata=json.dumps(metadata),
            user_address=current_user["address"]
        )

        return {
            "dataset_id": dataset_id,
            "ipfs_hash": ipfs_hash,
            "metadata": metadata,
            "message": "Dataset uploaded successfully"
        }

    except Exception as e:
        logger.error(f"Dataset upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/api/v1/datasets/{dataset_id}/download")
async def download_dataset(
    dataset_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Download a dataset (requires purchase or ownership)"""
    try:
        # Check access rights
        stacks_service = app.state.stacks_service
        has_access = await stacks_service.check_dataset_access(
            dataset_id, current_user["address"]
        )

        if not has_access:
            raise HTTPException(
                status_code=403,
                detail="Access denied. Purchase required."
            )

        # Get dataset info
        dataset_info = await stacks_service.get_dataset(dataset_id)
        if not dataset_info:
            raise HTTPException(status_code=404, detail="Dataset not found")

        # Download from IPFS
        ipfs_service = app.state.ipfs_service
        ipfs_hash = dataset_info["uri"].replace("ipfs://", "")
        file_data = await ipfs_service.download_file(ipfs_hash)

        # Return file as streaming response
        def generate():
            yield file_data

        metadata = json.loads(dataset_info["metadata"])
        filename = f"dataset_{dataset_id}.{metadata.get('file_type', 'csv')}"

        return StreamingResponse(
            generate(),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dataset download failed: {e}")
        raise HTTPException(status_code=500, detail="Download failed")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
