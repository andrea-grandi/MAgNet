from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode

from .state import AgentState
from chat_agent import nodes
from chat_agent import tools


def build_graph() -> CompiledStateGraph:
    """Create a LangGraph for the conversation flow."""
    
    graph = StateGraph(AgentState)
    tool_node = ToolNode(tools=tools)

    graph.set_entry_point("agent")

    graph.add_node("agent", nodes.model_call_node)
    graph.add_node("tools", tools.tool_node)

    graph.add_conditional_edges(
        source="agent",
        path=nodes.maybe_call_tool,
        path_map={
            "continue": "tools",
            "end": END
        }
    )

    graph.add_edge("tool", "agent")

    return graph.compile()
