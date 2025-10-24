from typing import Any, Dict
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage
from langsmith import traceable

from logic.graph import make_graph


class Agent:
    def __init__(self):
        """Initialize the supervisor agent. The graph will be created lazily on first use."""
        self._graph = None

    async def _ensure_graph(self):
        """Ensure the graph is initialized."""

        if self._graph is None:
            self._graph = await make_graph()
        return self._graph
    
    async def run(self, user_prompt: str, thread_id: str) -> str:
        """Run the supervisor agent with the given user prompt and thread ID.
        
        The supervisor will analyze the request and route it to the appropriate
        specialized agent (Math, Coding, or Translation).
        
        Args:
            user_prompt: The user's input message
            thread_id: Thread ID for state persistence
            
        Returns:
            The final response after agent processing
        """
        
        graph = await self._ensure_graph()
        
        config: RunnableConfig = {
            "configurable": {"thread_id": thread_id},
            "run_name": f"Supervisor-{thread_id}",
            "metadata": {
                "thread_id": thread_id,
                "user_prompt": user_prompt[:100], 
                "agent_type": "supervisor",
                "protocol": "a2a"
            },
            "tags": ["supervisor", "a2a", "multi-agent"]
        }
        
        result = await graph.ainvoke(
            {"messages": [HumanMessage(content=user_prompt)], "next_agent": ""},
            config=config
        )
        
        if "messages" in result and result["messages"]:
            responses = []
            for message in result["messages"]:
                if hasattr(message, "type") and message.type == "human":
                    continue
                    
                content = None
                if hasattr(message, "content"):
                    content = message.content
                elif isinstance(message, dict) and "content" in message:
                    content = message["content"]
                
                if content:
                    responses.append(str(content))
            
            if responses:
                return responses[-1]
        
        return "No response generated."