from typing import TypedDict, Any, Dict, List


class AgentState(TypedDict, total=False):
    thread_id: str
    raw_text: str
    input_is_json: bool
    request: Dict[str, Any]  
    tool_to_call: List[str]
    wx: Dict[str, Any]
    result: Dict[str, Any]