import os
import json
import httpx

from typing import Any, Dict, List, Optional
from fastmcp.exceptions import ToolError

from .models import FlightInfoInput, FlightInfoOutput


async def get_flight_info(req: FlightInfoInput) -> FlightInfoOutput:
    """Get flight information from a mock external API."""

    # Mock response for demonstration purposes
    mock_response = {
        "city": req.city,
        "date": req.date,
        "time": req.time,
        "flight_id": "AB123",
        "status": "On Time",
        "departure": "2024-10-01T10:00:00Z",
        "arrival": "2024-10-01T14:00:00Z",
        "duration": "4h",
        "details": "Gate 5, Boarding at 09:30 AM" if req.include_details else None
    }

    return FlightInfoOutput(
        api_version="1",
        flight_id=mock_response["flight_id"],
        status=mock_response["status"],
        departure=mock_response["departure"],
        arrival=mock_response["arrival"],
        duration=mock_response["duration"],
        details=mock_response["details"]
    )