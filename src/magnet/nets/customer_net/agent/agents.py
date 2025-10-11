import asyncio

from langgraph.prebuilt import create_react_agent
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from typing import Dict, Any, Optional

from .configs import *
from .handoffs import *
from .clients import FLIGHT_MCP_CLIENT, HOTEL_MCP_CLIENT
from .models import FlightSearchInput, HotelSearchInput


# Create ChatOpenAI models  
orchestrator_model = ChatOpenAI(
    model=ORCHESTRATOR_CONFIG.model_name,
    temperature=ORCHESTRATOR_CONFIG.temperature,
)

hotel_assistant_model = ChatOpenAI(
    model=HOTEL_ASSISTANT_CONFIG.model_name,
    temperature=HOTEL_ASSISTANT_CONFIG.temperature,
)

flight_assistant_model = ChatOpenAI(
    model=FLIGHT_ASSISTANT_CONFIG.model_name,
    temperature=FLIGHT_ASSISTANT_CONFIG.temperature,
)


# Create synchronous wrapper functions that execute async calls
def search_flights_sync(
    city: str,
    date: str,
    time: Optional[str] = None,
    include_details: bool = False,
) -> Dict[str, Any]:
    """Synchronous wrapper for flight search."""

    return asyncio.run(
        FLIGHT_MCP_CLIENT.search_flights(
            city=city,
            date=date,
            time=time,
            include_details=include_details
        )
    )

def search_hotels_sync(
    location: str,
    check_in: str,
    check_out: str,
    guests: int = 1,
) -> Dict[str, Any]:
    """Synchronous wrapper for hotel search."""

    return asyncio.run(
        HOTEL_MCP_CLIENT.search_hotels(
            location=location,
            check_in=check_in,
            check_out=check_out,
            guests=guests
        )
    )

# Create structured tools using the sync wrappers
flight_search_tool = StructuredTool(
    name="search_flights",
    description="Search for flights to a destination city on a specific date. Returns available flight information.",
    args_schema=FlightSearchInput,
    func=search_flights_sync,
)

hotel_search_tool = StructuredTool(
    name="search_hotels",
    description="Search for hotels in a location for specific check-in and check-out dates. Returns available hotel information.",
    args_schema=HotelSearchInput,
    func=search_hotels_sync,
)


orchestrator = create_react_agent(
    model=orchestrator_model,
    tools=[transfer_to_hotel_assistant, transfer_to_flight_assistant],
    prompt=ORCHESTRATOR_PROMPT,
    name=ORCHESTRATOR_CONFIG.name,
)

hotel_assistant = create_react_agent(
    model=hotel_assistant_model,
    tools=[hotel_search_tool, transfer_to_flight_assistant],
    prompt=HOTEL_ASSISTANT_PROMPT,
    name=HOTEL_ASSISTANT_CONFIG.name,
)

flight_assistant = create_react_agent(
    model=flight_assistant_model,
    tools=[flight_search_tool, transfer_to_hotel_assistant],
    prompt=FLIGHT_ASSISTANT_PROMPT,
    name=FLIGHT_ASSISTANT_CONFIG.name,
)