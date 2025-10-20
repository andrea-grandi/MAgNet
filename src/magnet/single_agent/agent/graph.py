import os

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent import nodes

load_dotenv()


def build_graph(mcp_server_url: str):
    """Builds and returns the agent's state graph."""

    graph = StateGraph(AgentState)

    graph.add_node("parse", nodes.parse)
    graph.add_node("call_mcp", nodes.call_mcp)
    graph.add_node("synthesize_response", nodes.synthesize_response)

    graph.set_entry_point("parse")
    
    graph.add_edge("parse", "call_mcp")
    graph.add_edge("call_mcp", "synthesize_response")
    graph.add_edge("synthesize_response", END)

    return graph.compile()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")
graph = build_graph(MCP_SERVER_URL) #type: ignore