from typing import Any, Dict
from langchain_core.runnables import RunnableConfig
from logic.graph import make_graph


class Agent:
    def __init__(self):
        """Initialize the agent. The graph will be created lazily on first use."""
        self._graph = None
    
    async def _ensure_graph(self):
        """Ensure the graph is initialized (lazy initialization)."""
        if self._graph is None:
            self._graph = await make_graph()
        return self._graph
    
    async def run(self, user_prompt: str, thread_id: str) -> str:
        """Run the agent with the given user prompt and thread ID."""
        
        graph = await self._ensure_graph()
        
        # LangGraph ReAct agent uses MessagesState with "messages" key
        # thread_id can be passed in the config for state persistence
        config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
        
        result = await graph.ainvoke(
            {"messages": [("user", user_prompt)]},
            config=config
        )
        
        if "messages" in result and result["messages"]:
            last_message = result["messages"][-1]
            if hasattr(last_message, "content"):
                return last_message.content
            elif isinstance(last_message, dict) and "content" in last_message:
                return last_message["content"]
        
        return "No response generated."