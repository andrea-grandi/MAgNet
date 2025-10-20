import os
import uuid

from dotenv import load_dotenv
from typing import Optional, Dict, Any
from fastmcp import Client 

load_dotenv()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")


class MCPClient:
    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        self.base_url = base_url or MCP_SERVER_URL
        if not self.base_url:
            raise RuntimeError("MCP_SERVER_URL not set in environment variables.")
        self.client = Client(self.base_url, timeout=timeout)


    """Here you can define methods to interact with the MCP server."""

    async def arithmetic(
        self,
        operation: str,
        numbers: list[float],
        trace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Call the arithmetic_tool on the MCP server.
        Example: operation='add', numbers=[1,2,3]
        """

        request_id = str(uuid.uuid4())
        payload = {
            "api_version": "1",
            "trace_id": trace_id or request_id,
            "operation": operation,
            "numbers": numbers
        }

        async with self.client as client:
            result = await client.call_tool("arithmetic_tool", payload)

        return vars(result.data)
    
    async def statistics(
        self,
        metric: str,
        numbers: list[float],
        trace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Call the statistics_tool on the MCP server.
        Example: metric='mean', numbers=[10,20,30]
        """
        
        request_id = str(uuid.uuid4())
        payload = {
            "api_version": "1",
            "trace_id": trace_id or request_id,
            "metric": metric,
            "numbers": numbers
        }

        async with self.client as client:
            result = await client.call_tool("statistics_tool", payload)

        return vars(result.data)

    async def close(self):
        if self.client.is_connected:
            await self.client.close()