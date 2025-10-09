from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage

from .llm import llm
from .state import AgentState


def model_call_node(state: AgentState) -> AgentState:
    messages = state["messages"]
    system_prompt = state["system_prompt"]
    response = llm.invoke([system_prompt] + messages)
    return {
        "messages": [response],
        "tool_results": state.get("tool_results", []),
        "metadata": state.get("metadata", {}),
        "token_usage": state.get("token_usage", {}),
        "step_count": state.get("step_count", 0),
        "system_prompt": system_prompt
    }

def maybe_call_tool(state: AgentState):
    last_msg = state["messages"][-1]
    if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
        return "continue"
    else:
        return "end"