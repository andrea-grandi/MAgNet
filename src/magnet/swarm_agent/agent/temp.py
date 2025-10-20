
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

model = ChatOpenAI(name="gpt-4o-mini")


client = MultiServerMCPClient(
    {
        "math": {
            "transport": "streamable_http",
            "url": "http://localhost:8990/mcp"
        },
    }
)

tools = client.get_tools()
agent = create_react_agent(model=model, tools=tools)
math_response = agent.ainvoke({"messages": "what's (3 + 5) x 12?"})