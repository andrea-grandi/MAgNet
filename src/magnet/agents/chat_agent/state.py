from typing import (
    Dict, 
    Any, 
    Optional, 
    TypedDict, 
    Annotated, 
    Sequence,
    Union,
)
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    tool_results: Optional[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]]
    token_usage: Optional[int]
    step_count: int
    system_prompt: Optional[Union[SystemMessage, str]]
