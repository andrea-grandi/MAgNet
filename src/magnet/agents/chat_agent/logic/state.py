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

