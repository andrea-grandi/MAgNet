import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langsmith import traceable

from .model import get_model

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

CODING_MCP_URL = os.getenv("CODING_MCP_URL", "http://localhost:8991/mcp")

@traceable(name="create_coding_agent", tags=["coding", "agent_creation", "mcp"])
async def create_coding_agent(model_name: str):
    """Create a coding specialized agent with coding MCP tools."""
    
    client = MultiServerMCPClient(
        {
            "coding": {
                "transport": "streamable_http",
                "url": CODING_MCP_URL
            },
        }
    )
    
    tools = await client.get_tools()
    model = get_model(model_name)
    agent = create_react_agent(model=model, tools=tools)
    
    return agent
