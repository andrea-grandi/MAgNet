import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8990/mcp")

async def make_graph():
    """Factory function to create the agent graph with MCP tools."""
    
    client = MultiServerMCPClient(
        {
            "calculator": {
                "transport": "streamable_http",
                "url": MCP_SERVER_URL
            },
        }
    )
    
    tools = await client.get_tools()
    model = ChatOpenAI(name="gpt-4o-mini")
    agent = create_react_agent(model=model, tools=tools)
    return agent

