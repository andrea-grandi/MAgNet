from typing import TypedDict, List, Dict, Optional


class AgentState(TypedDict):
    """State for the LangGraph agent."""

    role: str
    mtype: List[str]
    qtype: List[str]
    ans_parser: str
    reply: Optional[str]
    answer: str
    question: Optional[str]
    llm_ip: Optional[str]
    prompt_tokens: int
    completion_tokens: int
    nums: int
    temperature: float
    top_p: float
    model: str
    
    