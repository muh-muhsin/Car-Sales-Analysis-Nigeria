"""
IPFS Storage Service
Handles file uploads and retrieval from IPFS network
"""

import asyncio
import json
import logging
import tempfile
import os
from typing import Dict, List, Optional, Any, BinaryIO
import httpx
import ipfshttpclient
from app.core.config import settings

logger = logging.getLogger(__name__)


class IPFSService:
    """Service for interacting with IPFS network"""
    
    def __init__(self):
        self.api_url = settings.IPFS_API_URL
        self.gateway_url = settings.IPFS_GATEWAY_URL
        self.client = None
        
    async def _get_client(self):
        """Get IPFS client connection"""
        if not self.client:
            try:
                self.client = ipfshttpclient.connect(self.api_url)
                # Test connection
                await asyncio.get_event_loop().run_in_executor(
                    None, self.client.version
                )
                logger.info("Connected to IPFS node")
            except Exception as e:
                logger.error(f"Failed to connect to IPFS: {e}")
                self.client = None
        return self.client
    
    async def upload_file(self, file_data: bytes, filename: str = None) -> Optional[str]:
        """Upload file to IPFS and return hash"""
        try:
            client = await self._get_client()
            if not client:
                raise Exception("IPFS client not available")
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file_data)
                temp_file_path = temp_file.name
            
            try:
                # Upload to IPFS
                result = await asyncio.get_event_loop().run_in_executor(
                    None, client.add, temp_file_path
                )
                
                ipfs_hash = result['Hash']
                logger.info(f"File uploaded to IPFS: {ipfs_hash}")
                
                # Pin the file to ensure it stays available
                await asyncio.get_event_loop().run_in_executor(
                    None, client.pin.add, ipfs_hash
                )
                
                return ipfs_hash
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"Failed to upload file to IPFS: {e}")
            return None
    
    async def upload_json(self, data: Dict[str, Any]) -> Optional[str]:
        """Upload JSON data to IPFS"""
        try:
            json_data = json.dumps(data, indent=2).encode('utf-8')
            return await self.upload_file(json_data, "data.json")
        except Exception as e:
            logger.error(f"Failed to upload JSON to IPFS: {e}")
            return None
    
    async def get_file(self, ipfs_hash: str) -> Optional[bytes]:
        """Retrieve file from IPFS"""
        try:
            client = await self._get_client()
            if not client:
                # Fallback to HTTP gateway
                return await self._get_file_via_gateway(ipfs_hash)
            
            # Get file via IPFS client
            result = await asyncio.get_event_loop().run_in_executor(
                None, client.cat, ipfs_hash
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to get file from IPFS: {e}")
            # Fallback to HTTP gateway
            return await self._get_file_via_gateway(ipfs_hash)
    
    async def _get_file_via_gateway(self, ipfs_hash: str) -> Optional[bytes]:
        """Retrieve file via HTTP gateway as fallback"""
        try:
            url = f"{self.gateway_url}/ipfs/{ipfs_hash}"
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.content
        except Exception as e:
            logger.error(f"Failed to get file via gateway: {e}")
            return None
    
    async def get_json(self, ipfs_hash: str) -> Optional[Dict[str, Any]]:
        """Retrieve and parse JSON from IPFS"""
        try:
            data = await self.get_file(ipfs_hash)
            if data:
                return json.loads(data.decode('utf-8'))
            return None
        except Exception as e:
            logger.error(f"Failed to get JSON from IPFS: {e}")
            return None
    
    async def pin_file(self, ipfs_hash: str) -> bool:
        """Pin file to ensure it stays available"""
        try:
            client = await self._get_client()
            if not client:
                return False
            
            await asyncio.get_event_loop().run_in_executor(
                None, client.pin.add, ipfs_hash
            )
            
            logger.info(f"File pinned: {ipfs_hash}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to pin file: {e}")
            return False
    
    async def unpin_file(self, ipfs_hash: str) -> bool:
        """Unpin file from IPFS"""
        try:
            client = await self._get_client()
            if not client:
                return False
            
            await asyncio.get_event_loop().run_in_executor(
                None, client.pin.rm, ipfs_hash
            )
            
            logger.info(f"File unpinned: {ipfs_hash}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unpin file: {e}")
            return False
    
    async def get_file_info(self, ipfs_hash: str) -> Optional[Dict[str, Any]]:
        """Get file information from IPFS"""
        try:
            client = await self._get_client()
            if not client:
                return None
            
            # Get file stats
            stats = await asyncio.get_event_loop().run_in_executor(
                None, client.object.stat, ipfs_hash
            )
            
            return {
                "hash": ipfs_hash,
                "size": stats.get("CumulativeSize", 0),
                "links": stats.get("NumLinks", 0),
                "blocks": stats.get("BlockSize", 0)
            }
            
        except Exception as e:
            logger.error(f"Failed to get file info: {e}")
            return None
    
    async def health_check(self) -> bool:
        """Check if IPFS service is healthy"""
        try:
            client = await self._get_client()
            if not client:
                return False
            
            # Test with version call
            await asyncio.get_event_loop().run_in_executor(
                None, client.version
            )
            
            return True
            
        except Exception as e:
            logger.error(f"IPFS health check failed: {e}")
            return False
