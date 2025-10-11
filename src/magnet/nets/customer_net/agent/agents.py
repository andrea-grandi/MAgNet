from langgraph.prebuilt import create_react_agent

from .configs import *
from .handoffs import *
from .mcp_clients import flight_mcp_client, hotel_mcp_client


orchestrator = create_react_agent(
    model=ORCHESTRATOR_CONFIG.model_name,
    tools=[transfer_to_hotel_assistant, transfer_to_flight_assistant],
    prompt=ORCHESTRATOR_PROMPT,
    name=ORCHESTRATOR_CONFIG.name,
)

hotel_assistant = create_react_agent(
    model=HOTEL_ASSISTANT_CONFIG.model_name,
    tools=[hotel_mcp_client.search_hotels, transfer_to_flight_assistant],
    prompt=HOTEL_ASSISTANT_PROMPT,
    name=HOTEL_ASSISTANT_CONFIG.name,
)

flight_assistant = create_react_agent(
    model=FLIGHT_ASSISTANT_CONFIG.model_name,
    tools=[flight_mcp_client.search_flights, transfer_to_hotel_assistant],
    prompt=FLIGHT_ASSISTANT_PROMPT,
    name=FLIGHT_ASSISTANT_CONFIG.name,
)