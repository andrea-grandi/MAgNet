from typing import TypedDict, List, Dict


class AgentState(TypedDict):
    """State for the LangGraph agent."""

    role: str
    mtype: str
    qtype: str
    question: str | None
    contexts: List[Dict[str, str]]
    reply: str | None
    answer: str
    prompt_tokens: int
    completion_tokens: int
    temperature: float
    top_p: int
    nums: int
    llm_ip: str | None