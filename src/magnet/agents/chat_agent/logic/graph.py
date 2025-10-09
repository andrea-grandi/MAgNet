from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph

from .state import AgentState
from . import nodes


def build_graph() -> CompiledStateGraph:
    """Create a LangGraph for the conversation flow."""
    
    graph = StateGraph(AgentState)
    graph.set_entry_point("agent")
    graph.add_node("agent", nodes.model_node)
    graph.set_finish_point("agent")

    return graph.compile()
