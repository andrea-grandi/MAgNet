"""Math Agent - Specialized in mathematical operations."""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

MATH_MCP_URL = os.getenv("MATH_MCP_URL", "http://localhost:8990/mcp")

async def create_math_agent():
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
    model = ChatOpenAI(name="gpt-4o-mini")
    agent = create_react_agent(model=model, tools=tools)
    
    return agent
