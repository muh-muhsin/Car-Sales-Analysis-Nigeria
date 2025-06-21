"""
Auth Microservice
Handles user authentication and authorization
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
import os
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Auth Microservice...")
    yield
    # Shutdown
    logger.info("Shutting down Auth Microservice...")

# Create FastAPI app
app = FastAPI(
    title="Cars360 Auth Microservice",
    description="Authentication and authorization service for Cars360",
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

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Cars360 Auth Microservice",
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
            "service": "auth"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.post("/login")
async def login(request: Request):
    """User login endpoint"""
    try:
        data = await request.json()
        wallet_address = data.get("wallet_address")
        signature = data.get("signature")
        
        if not wallet_address or not signature:
            raise HTTPException(status_code=400, detail="Missing wallet address or signature")
        
        # Verify signature (simplified for example)
        # In a real implementation, verify the signature against the wallet address
        
        # Generate JWT token
        token = f"mock_token_for_{wallet_address}"
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "address": wallet_address,
                "profile": {
                    "username": f"user_{wallet_address[:8]}",
                }
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@app.get("/verify")
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    try:
        token = credentials.credentials
        
        # In a real implementation, verify the JWT token
        # For this example, we'll just check if it starts with "mock_token_for_"
        
        if not token.startswith("mock_token_for_"):
            raise HTTPException(status_code=401, detail="Invalid token")
        
        wallet_address = token.replace("mock_token_for_", "")
        
        return {
            "valid": True,
            "user": {
                "address": wallet_address,
                "profile": {
                    "username": f"user_{wallet_address[:8]}",
                }
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(status_code=500, detail="Token verification failed")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )