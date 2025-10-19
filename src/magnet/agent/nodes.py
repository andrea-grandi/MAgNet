import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from dotenv import load_dotenv

from .state import AgentState
from .parser import Parser
from .client import MCPClient

load_dotenv()

parser = Parser()
caller = MCPClient()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """system prompt text here"""
        ),
    ]
)
chain = prompt | llm


async def parse(state: AgentState) -> AgentState:
    raw = state.get("raw_text", "") or ""
    extracted = await parser.parse(raw)
    state["request"] = extracted or {}
    return state

async def call_mcp(state: AgentState) -> AgentState:
    """Calls the MCP backend with the request data."""

    #TODO
    
    pass

async def synthesize_response(state: AgentState) -> AgentState:
    """Synthesizes a final response based on MCP results."""

    #TODO

    pass