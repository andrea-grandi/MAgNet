eacimport asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.client import MultiServerMCPClient

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

model = ChatOpenAI(name="gpt-4o-mini")


async def make_graph():
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "streamable_http",
                "url": "http://localhost:8990/mcp"
        },
    }
    )

    tools = await client.get_tools()
    agent = create_react_agent(model=model, tools=tools)
    return agent


if __name__ == "__main__":
    asyncio.run(make_graph())