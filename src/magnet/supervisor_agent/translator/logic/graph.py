import os

from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from .model import get_model

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

TRANSLATION_MCP_URL = os.getenv("TRANSLATION_MCP_URL", "http://localhost:8992/mcp")
TRANSLATION_MODEL = os.getenv("TRANSLATION_MODEL", "gpt-4o-mini")


async def create_translation_agent(model_name: str):
    """Create a translation specialized agent with translation MCP tools."""

    tools = []
    """
    client = MultiServerMCPClient(
        {
            "translation": {
                "transport": "streamable_http",
                "url": TRANSLATION_MCP_URL
            },
        }
    )
    
    tools = await client.get_tools()
    """
    model = get_model(model_name)
    agent = create_react_agent(model=model, tools=tools)
    
    return agent


async def make_graph():
    """Factory function to create the translator agent graph.
    
    This creates a LangGraph ReAct agent.
    The agent can handle text translation, language detection, and multilingual tasks.
    """
    
    print(f"[TRANSLATOR] Initializing translator agent with model: {TRANSLATION_MODEL}")
    graph = await create_translation_agent(TRANSLATION_MODEL)
    print(f"[TRANSLATOR] Translator agent graph initialized successfully")
    
    return graph
