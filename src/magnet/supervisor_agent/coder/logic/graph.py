import os

from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from .model import get_model

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

CODING_MCP_URL = os.getenv("CODING_MCP_URL", "http://localhost:8991/mcp")
CODING_MODEL = os.getenv("CODING_MODEL", "gpt-4o-mini")


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


async def make_graph():
    """Factory function to create the coder agent graph.
    
    This creates a LangGraph ReAct agent with MCP coding tools.
    The agent can handle code generation, review, debugging, and programming tasks.
    """
    
    print(f"[CODER] Initializing coder agent with model: {CODING_MODEL}")
    graph = await create_coding_agent(CODING_MODEL)
    print(f"[CODER] Coder agent graph initialized successfully")
    
    return graph
