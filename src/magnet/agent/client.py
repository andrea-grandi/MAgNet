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


    async def close(self):
        if self.client.is_connected:
            await self.client.close()