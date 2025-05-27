"""
Stacks Blockchain Service
Handles interactions with Stacks blockchain and smart contracts
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)


class StacksService:
    """Service for interacting with Stacks blockchain"""
    
    def __init__(self):
        self.api_url = settings.STACKS_API_URL
        self.network = settings.STACKS_NETWORK
        self.contract_address = settings.CONTRACT_ADDRESS
        
    async def get_network_status(self) -> bool:
        """Check if blockchain network is accessible"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}/v2/info")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to check network status: {e}")
            return False
    
    async def get_dataset(self, dataset_id: int) -> Optional[Dict[str, Any]]:
        """Get dataset information from blockchain"""
        try:
            # Call read-only function on dataset-registry contract
            function_args = [f"u{dataset_id}"]
            
            response = await self._call_read_only_function(
                contract_name="dataset-registry",
                function_name="get-dataset",
                function_args=function_args
            )
            
            if response and "result" in response:
                return self._parse_clarity_value(response["result"])
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get dataset {dataset_id}: {e}")
            return None
    
    async def register_dataset(
        self, 
        uri: str, 
        price: int, 
        metadata: str, 
        user_address: str
    ) -> Optional[int]:
        """Register a new dataset on blockchain"""
        try:
            # This would typically be called from frontend with user's wallet
            # For now, we'll return a mock dataset ID
            # In production, this would interact with user's wallet
            
            logger.info(f"Dataset registration requested: {uri}, {price}, {user_address}")
            
            # Mock implementation - in reality this would be handled by frontend
            # Return a mock dataset ID
            return 1
            
        except Exception as e:
            logger.error(f"Failed to register dataset: {e}")
            return None
    
    async def check_dataset_access(self, dataset_id: int, user_address: str) -> bool:
        """Check if user has access to dataset"""
        try:
            function_args = [f"u{dataset_id}", f"'{user_address}"]
            
            response = await self._call_read_only_function(
                contract_name="dataset-registry",
                function_name="has-access",
                function_args=function_args
            )
            
            if response and "result" in response:
                return self._parse_clarity_value(response["result"]) == True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to check access for dataset {dataset_id}: {e}")
            return False
    
    async def get_marketplace_stats(self) -> Dict[str, Any]:
        """Get marketplace statistics from blockchain"""
        try:
            response = await self._call_read_only_function(
                contract_name="marketplace",
                function_name="get-marketplace-stats",
                function_args=[]
            )
            
            if response and "result" in response:
                stats = self._parse_clarity_value(response["result"])
                return {
                    "total_volume": stats.get("total-volume", 0),
                    "total_transactions": stats.get("total-transactions", 0)
                }
            
            return {"total_volume": 0, "total_transactions": 0}
            
        except Exception as e:
            logger.error(f"Failed to get marketplace stats: {e}")
            return {"total_volume": 0, "total_transactions": 0}
    
    async def get_user_datasets(self, user_address: str) -> List[int]:
        """Get list of datasets owned by user"""
        try:
            function_args = [f"'{user_address}"]
            
            response = await self._call_read_only_function(
                contract_name="dataset-registry",
                function_name="get-user-datasets",
                function_args=function_args
            )
            
            if response and "result" in response:
                result = self._parse_clarity_value(response["result"])
                return result.get("dataset-ids", [])
            
            return []
            
        except Exception as e:
            logger.error(f"Failed to get user datasets for {user_address}: {e}")
            return []
    
    async def get_user_purchases(self, user_address: str) -> List[int]:
        """Get list of datasets purchased by user"""
        try:
            function_args = [f"'{user_address}"]
            
            response = await self._call_read_only_function(
                contract_name="dataset-registry",
                function_name="get-user-purchases",
                function_args=function_args
            )
            
            if response and "result" in response:
                result = self._parse_clarity_value(response["result"])
                return result.get("dataset-ids", [])
            
            return []
            
        except Exception as e:
            logger.error(f"Failed to get user purchases for {user_address}: {e}")
            return []
    
    async def _call_read_only_function(
        self, 
        contract_name: str, 
        function_name: str, 
        function_args: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Call a read-only function on a smart contract"""
        try:
            url = f"{self.api_url}/v2/contracts/call-read/{self.contract_address}/{contract_name}/{function_name}"
            
            payload = {
                "sender": self.contract_address,
                "arguments": function_args
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Contract call failed: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Failed to call contract function {function_name}: {e}")
            return None
    
    def _parse_clarity_value(self, clarity_value: Any) -> Any:
        """Parse Clarity value to Python value"""
        if isinstance(clarity_value, dict):
            if clarity_value.get("type") == "uint":
                return int(clarity_value.get("value", 0))
            elif clarity_value.get("type") == "bool":
                return clarity_value.get("value") == "true"
            elif clarity_value.get("type") == "principal":
                return clarity_value.get("value")
            elif clarity_value.get("type") == "string-utf8":
                return clarity_value.get("value")
            elif clarity_value.get("type") == "tuple":
                result = {}
                for key, value in clarity_value.get("value", {}).items():
                    result[key] = self._parse_clarity_value(value)
                return result
            elif clarity_value.get("type") == "list":
                return [self._parse_clarity_value(item) for item in clarity_value.get("value", [])]
            elif clarity_value.get("type") == "some":
                return self._parse_clarity_value(clarity_value.get("value"))
            elif clarity_value.get("type") == "none":
                return None
        
        return clarity_value
