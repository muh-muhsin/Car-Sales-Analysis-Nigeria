"""
Datasets Microservice
Handles dataset management, storage, and retrieval
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from contextlib import asynccontextmanager
import uvicorn
import os
from typing import List, Optional, Dict, Any
import json
from datetime import datetime
import logging
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Datasets Microservice...")
    yield
    # Shutdown
    logger.info("Shutting down Datasets Microservice...")

# Create FastAPI app
app = FastAPI(
    title="Cars360 Datasets Microservice",
    description="Dataset management service for Cars360",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth service URL
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth:8001")
# Blockchain service URL (will be implemented later)
BLOCKCHAIN_SERVICE_URL = os.getenv("BLOCKCHAIN_SERVICE_URL", "http://blockchain:8004")

async def get_current_user(request: Request):
    """Get current user from auth service"""
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/verify",
                headers={"Authorization": auth_header}
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token")
                
            return response.json()["user"]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(status_code=500, detail="Authentication service unavailable")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Cars360 Datasets Microservice",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "datasets"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/datasets")
async def get_datasets(
    skip: int = 0, 
    limit: int = 10,
    user: Dict = Depends(get_current_user)
):
    """Get list of datasets"""
    try:
        # Mock implementation - in a real service, this would query a database
        datasets = [
            {
                "id": 1,
                "title": "Nigerian Car Sales 2022",
                "description": "Comprehensive dataset of car sales in Nigeria for 2022",
                "owner": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
                "price": 100,
                "created_at": "2023-01-15T12:00:00Z",
                "records_count": 5000,
                "tags": ["cars", "sales", "nigeria", "2022"]
            },
            {
                "id": 2,
                "title": "Lagos Vehicle Registration Data",
                "description": "Vehicle registration data from Lagos State",
                "owner": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
                "price": 150,
                "created_at": "2023-02-20T14:30:00Z",
                "records_count": 3500,
                "tags": ["registration", "lagos", "vehicles"]
            }
        ]
        
        return {
            "items": datasets[skip:skip+limit],
            "total": len(datasets),
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        logger.error(f"Failed to get datasets: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve datasets")

@app.get("/datasets/{dataset_id}")
async def get_dataset(
    dataset_id: int,
    user: Dict = Depends(get_current_user)
):
    """Get dataset by ID"""
    try:
        # Mock implementation - in a real service, this would query a database
        dataset = {
            "id": dataset_id,
            "title": "Nigerian Car Sales 2022",
            "description": "Comprehensive dataset of car sales in Nigeria for 2022",
            "owner": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
            "price": 100,
            "created_at": "2023-01-15T12:00:00Z",
            "records_count": 5000,
            "tags": ["cars", "sales", "nigeria", "2022"],
            "preview_data": [
                {"make": "Toyota", "model": "Camry", "year": 2020, "price": 15000},
                {"make": "Honda", "model": "Accord", "year": 2019, "price": 14000},
                {"make": "Ford", "model": "Focus", "year": 2021, "price": 13000}
            ]
        }
        
        return dataset
    except Exception as e:
        logger.error(f"Failed to get dataset {dataset_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve dataset")

@app.post("/datasets/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    price: int = Form(...),
    tags: str = Form(""),
    user: Dict = Depends(get_current_user)
):
    """Upload a new dataset"""
    try:
        # Validate file type
        if not file.filename.endswith(('.csv', '.xlsx', '.json')):
            raise HTTPException(
                status_code=400,
                detail="Only CSV, XLSX, and JSON files are supported"
            )
        
        # Mock implementation - in a real service, this would process the file
        # and store it in a database or file storage system
        
        # Mock dataset ID
        dataset_id = 3
        
        # Mock IPFS hash
        ipfs_hash = "QmXyZ123456789"
        
        # Create metadata
        metadata = {
            "title": title,
            "description": description,
            "tags": tags.split(",") if tags else [],
            "file_type": file.filename.split(".")[-1],
            "upload_date": datetime.utcnow().isoformat(),
            "records_count": 1000,  # Mock value
            "ipfs_hash": ipfs_hash
        }
        
        return {
            "dataset_id": dataset_id,
            "ipfs_hash": ipfs_hash,
            "metadata": metadata,
            "message": "Dataset uploaded successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dataset upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/datasets/{dataset_id}/download")
async def download_dataset(
    dataset_id: int,
    user: Dict = Depends(get_current_user)
):
    """Download a dataset (requires purchase or ownership)"""
    try:
        # Mock implementation - in a real service, this would check access rights
        # and download the file from storage
        
        # Mock file data
        file_data = b'{"mock": "data"}'
        
        def generate():
            yield file_data
        
        return StreamingResponse(
            generate(),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=dataset_{dataset_id}.json"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dataset download failed: {e}")
        raise HTTPException(status_code=500, detail="Download failed")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )