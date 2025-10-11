import os
import uuid

from dotenv import load_dotenv
from typing import Optional, Dict, Any
from fastmcp import Client
from .configs import MCPClientConfig
from .configs import FLIGHT_MCP_CONFIG, HOTEL_MCP_CONFIG

load_dotenv()

FLIGHT_MCP_URL = os.getenv("FLIGHT_MCP_URL")
HOTEL_MCP_URL = os.getenv("HOTEL_MCP_URL")


class FlightMCPClient:
    def __init__(self, configs: MCPClientConfig):
        self.server_url = configs.server_url 
        if not self.server_url:
            raise RuntimeError("FLIGHT_MCP_URL not defined in .env")
        self.client = Client(self.server_url, timeout=configs.timeout)

    async def search_flights(
        self, 
        city: str,
        date: str,
        time: Optional[str] = None,
        include_details: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Calls the flight MCP to search for flights.
        
        Args:
            city: The city to search flights for
            date: The date for the flight (YYYY-MM-DD format)
            time: Optional time for the flight
            include_details: Whether to include detailed flight information
        """

        mcp_payload = {
            "api_version": "1",
            "trace_id": "flight-agent-" + str(uuid.uuid4()),
            "city": city,
            "date": date,
            "time": time,
            "include_details": include_details
        }

        print("FLIGHT MCP PAYLOAD:", mcp_payload)
        print("=" * 60)

        try:
            async with self.client as session:
                result = await session.call_tool(
                    "get_flight_info_tool",
                    {"payload": mcp_payload}
                )
            
            # Extract response based on result type
            if hasattr(result, 'content') and result.content:
                first_content = result.content[0]
                response = getattr(first_content, 'text', str(first_content))
            elif hasattr(result, 'data'):
                response = vars(result.data)
            else:
                response = str(result)
                
            print("FLIGHT MCP RESPONSE:", response)
            print("=" * 60)
            return {"result": response}
        except Exception as e:
            error_msg = f"Error calling flight MCP: {type(e).__name__}: {str(e)}"
            print("FLIGHT MCP ERROR:", error_msg)
            print("=" * 60)
            return {"error": error_msg}

    async def close(self):
        if self.client.is_connected:
            await self.client.close()


class HotelMCPClient:
    def __init__(self, configs: MCPClientConfig):
        self.server_url = configs.server_url
        if not self.server_url:
            raise RuntimeError("HOTEL_MCP_URL not defined in .env")
        self.client = Client(self.server_url, timeout=configs.timeout)

    async def search_hotels(
        self,
        location: str,
        check_in: str,
        check_out: str,
        guests: int = 1,
        **kwargs
    ) -> Dict[str, Any]:
        """Calls the hotel MCP service to search for hotels.
        
        Args:
            location: The location to search hotels in
            check_in: Check-in date (YYYY-MM-DD format)
            check_out: Check-out date (YYYY-MM-DD format)
            guests: Number of guests
        """

        mcp_payload = {
            "api_version": "1",
            "trace_id": "hotel-agent-" + str(uuid.uuid4()),
            "location": location,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests
        }

        print("HOTEL MCP PAYLOAD:", mcp_payload)
        print("=" * 60)

        try:
            async with self.client as session:
                result = await session.call_tool(
                    "get_hotel_tool",
                    {"payload": mcp_payload}
                )
            
            # Extract response based on result type
            if hasattr(result, 'content') and result.content:
                first_content = result.content[0]
                response = getattr(first_content, 'text', str(first_content))
            elif hasattr(result, 'data'):
                response = vars(result.data)
            else:
                response = str(result)
                
            print("HOTEL MCP RESPONSE:", response)
            print("=" * 60)
            return {"result": response}
        except Exception as e:
            error_msg = f"Error calling hotel MCP: {type(e).__name__}: {str(e)}"
            print("HOTEL MCP ERROR:", error_msg)
            print("=" * 60)
            return {"error": error_msg}

    async def close(self):
        if self.client.is_connected:
            await self.client.close()


# Create singleton instances of the MCP clients
flight_mcp_client = FlightMCPClient(FLIGHT_MCP_CONFIG)
hotel_mcp_client = HotelMCPClient(HOTEL_MCP_CONFIG)