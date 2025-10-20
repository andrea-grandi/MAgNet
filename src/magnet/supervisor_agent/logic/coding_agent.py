import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

CODING_MCP_URL = os.getenv("CODING_MCP_URL", "http://localhost:8991/mcp")

async def create_coding_agent():
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
    model = ChatOpenAI(name="gpt-4o-mini")
    agent = create_react_agent(model=model, tools=tools)
    
    return agent
