"""Translation Agent - Specialized in text translation and language detection."""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

TRANSLATION_MCP_URL = os.getenv("TRANSLATION_MCP_URL", "http://localhost:8992/mcp")

async def create_translation_agent():
    """Create a translation specialized agent with translation MCP tools."""
    
    client = MultiServerMCPClient(
        {
            "translation": {
                "transport": "streamable_http",
                "url": TRANSLATION_MCP_URL
            },
        }
    )
    
    tools = await client.get_tools()
    model = ChatOpenAI(name="gpt-4o-mini")
    agent = create_react_agent(model=model, tools=tools)
    
    return agent
