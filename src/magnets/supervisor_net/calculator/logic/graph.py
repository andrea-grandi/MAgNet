import os

from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from .model import get_model

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

MATH_MCP_URL = os.getenv("MATH_MCP_URL", "http://localhost:8990/mcp")
MATH_MODEL = os.getenv("MATH_MODEL", "gpt-4o-mini")


async def create_math_agent(model_name: str):
    """Create a math specialized agent with calculator MCP tools."""
    
    client = MultiServerMCPClient(
        {
            "calculator": {
                "transport": "streamable_http",
                "url": MATH_MCP_URL
            },
        }
    )
    
    tools = await client.get_tools()
    model = get_model(model_name)
    agent = create_react_agent(model=model, tools=tools)
    
    return agent


async def make_graph():
    """Factory function to create the calculator agent graph.
    
    This creates a LangGraph ReAct agent with MCP calculator tools.
    The agent can perform mathematical operations and statistical calculations.
    """
    
    print(f"[CALCULATOR] Initializing calculator agent with model: {MATH_MODEL}")
    graph = await create_math_agent(MATH_MODEL)
    print(f"[CALCULATOR] Calculator agent graph initialized successfully")
    
    return graph
