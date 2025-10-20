import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from dotenv import load_dotenv

from .state import AgentState
from .parser import Parser
from .client import CalculatorMCPClient

load_dotenv()

parser = Parser()
caller = CalculatorMCPClient()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert in math.
            Your task is to translate raw data from a tool into a clear,
            concise, and technical response. Be directive and informative.
            The tool called was '{tool_name}' and the data returned was 
            '{backend_data}'. Do not make up data."""
        ),
    ]
)
chain = prompt | llm


async def parse(state: AgentState) -> AgentState:
    raw = state.get("raw_text", "") 
    extracted = await parser.parse(raw)

    if not extracted:
        return {
            "backend_result": {"error": "I couldn't identify a clear action or there is missing data in your question."},
            "tool_to_call": "no_tool_found"
        }
    
    state["request"] = extracted or {}
    return state

async def should_continue(state: AgentState) -> AgentState:
    last_message = state.get("request", {})[-1]
    print(last_message)
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

async def call_mcp(state: AgentState) -> AgentState:
    """Calls the MCP backend with the request data."""
    request = state.get("request", {}) or {}
    
    pass

async def synthesize_response(state: AgentState) -> AgentState:
    """Synthesizes a final response based on MCP results."""

    pass