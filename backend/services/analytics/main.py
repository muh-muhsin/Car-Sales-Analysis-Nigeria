"""
Analytics Microservice
Handles data analytics and visualization
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
from typing import List, Dict, Any, Optional
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
    logger.info("Starting Analytics Microservice...")
    yield
    # Shutdown
    logger.info("Shutting down Analytics Microservice...")

# Create FastAPI app
app = FastAPI(
    title="Cars360 Analytics Microservice",
    description="Data analytics service for Cars360",
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
# Datasets service URL
DATASETS_SERVICE_URL = os.getenv("DATASETS_SERVICE_URL", "http://datasets:8002")

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
        "message": "Cars360 Analytics Microservice",
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
            "service": "analytics"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/analytics/market-overview")
async def get_market_overview(
    user: Dict = Depends(get_current_user)
):
    """Get market overview analytics"""
    try:
        # Mock implementation - in a real service, this would analyze data
        # from the datasets service or a database
        
        return {
            "total_listings": 15000,
            "average_price": 12500,
            "price_trends": [
                {"month": "Jan", "average_price": 12000},
                {"month": "Feb", "average_price": 12200},
                {"month": "Mar", "average_price": 12400},
                {"month": "Apr", "average_price": 12500},
                {"month": "May", "average_price": 12600},
                {"month": "Jun", "average_price": 12700}
            ],
            "popular_brands": [
                {"brand": "Toyota", "count": 3500},
                {"brand": "Honda", "count": 2800},
                {"brand": "Ford", "count": 2200},
                {"brand": "Nissan", "count": 1800},
                {"brand": "Hyundai", "count": 1500}
            ],
            "popular_models": [
                {"model": "Camry", "count": 1200},
                {"model": "Accord", "count": 1100},
                {"model": "Corolla", "count": 1000},
                {"model": "Civic", "count": 900},
                {"model": "Focus", "count": 800}
            ],
            "last_updated": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get market overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve market overview")

@app.get("/analytics/price-distribution")
async def get_price_distribution(
    user: Dict = Depends(get_current_user)
):
    """Get price distribution analytics"""
    try:
        # Mock implementation - in a real service, this would analyze data
        # from the datasets service or a database
        
        return {
            "distribution": [
                {"range": "0-5000", "count": 2500},
                {"range": "5001-10000", "count": 5000},
                {"range": "10001-15000", "count": 4000},
                {"range": "15001-20000", "count": 2000},
                {"range": "20001-25000", "count": 1000},
                {"range": "25001+", "count": 500}
            ],
            "median_price": 12000,
            "average_price": 12500,
            "min_price": 1000,
            "max_price": 50000,
            "last_updated": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get price distribution: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve price distribution")

@app.get("/analytics/regional-data")
async def get_regional_data(
    user: Dict = Depends(get_current_user)
):
    """Get regional data analytics"""
    try:
        # Mock implementation - in a real service, this would analyze data
        # from the datasets service or a database
        
        return {
            "regions": [
                {
                    "name": "Lagos",
                    "listings_count": 5000,
                    "average_price": 13000,
                    "popular_brands": ["Toyota", "Honda", "Nissan"]
                },
                {
                    "name": "Abuja",
                    "listings_count": 3000,
                    "average_price": 14000,
                    "popular_brands": ["Toyota", "Ford", "Mercedes"]
                },
                {
                    "name": "Port Harcourt",
                    "listings_count": 2000,
                    "average_price": 12000,
                    "popular_brands": ["Toyota", "Honda", "Hyundai"]
                },
                {
                    "name": "Kano",
                    "listings_count": 1500,
                    "average_price": 10000,
                    "popular_brands": ["Toyota", "Nissan", "Hyundai"]
                },
                {
                    "name": "Ibadan",
                    "listings_count": 1200,
                    "average_price": 11000,
                    "popular_brands": ["Toyota", "Honda", "Kia"]
                }
            ],
            "last_updated": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get regional data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve regional data")

@app.get("/analytics/dataset/{dataset_id}")
async def analyze_dataset(
    dataset_id: int,
    user: Dict = Depends(get_current_user)
):
    """Analyze a specific dataset"""
    try:
        # In a real implementation, this would fetch the dataset from the datasets service
        # and perform analysis on it
        
        # Mock implementation
        return {
            "dataset_id": dataset_id,
            "summary_stats": {
                "total_records": 5000,
                "numerical_columns": {
                    "price": {
                        "mean": 12500,
                        "median": 12000,
                        "min": 1000,
                        "max": 50000,
                        "std_dev": 5000
                    },
                    "year": {
                        "mean": 2018,
                        "median": 2019,
                        "min": 2010,
                        "max": 2023,
                        "std_dev": 3
                    }
                },
                "categorical_columns": {
                    "brand": {
                        "unique_values": 25,
                        "top_values": [
                            {"value": "Toyota", "count": 1500},
                            {"value": "Honda", "count": 1200},
                            {"value": "Ford", "count": 800}
                        ]
                    },
                    "model": {
                        "unique_values": 150,
                        "top_values": [
                            {"value": "Camry", "count": 600},
                            {"value": "Accord", "count": 500},
                            {"value": "Corolla", "count": 450}
                        ]
                    },
                    "color": {
                        "unique_values": 12,
                        "top_values": [
                            {"value": "Black", "count": 1200},
                            {"value": "White", "count": 1100},
                            {"value": "Silver", "count": 900}
                        ]
                    }
                }
            },
            "correlations": [
                {"variables": ["year", "price"], "correlation": 0.75},
                {"variables": ["mileage", "price"], "correlation": -0.65}
            ],
            "last_updated": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to analyze dataset {dataset_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze dataset")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
        reload=True,
        log_level="info"
    )