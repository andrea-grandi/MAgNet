from typing import Any, AsyncGenerator, Dict

from langchain_core.messages import BaseMessage, HumanMessage

import sys
from pathlib import Path

# Add logic directory to path
logic_path = Path(__file__).parent.parent / "logic"
sys.path.insert(0, str(logic_path))

from logic import nodes
from logic.state import AgentState


class ChatAgent:
    async def stream(self, user_input: HumanMessage) -> AsyncGenerator[Dict[str, Any], None]:
        state: AgentState = {
            "messages": [user_input],
        }
        yield {"content": "Analyzing input...", "is_task_complete": False}
        state = await nodes.model_node(state)
        
        yield {"content": state["messages"][-1].content, "is_task_complete": True}
        final_text = state["messages"][-1].content

        yield {"content": final_text, "is_task_complete": True}
    

