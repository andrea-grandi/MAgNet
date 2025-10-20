from typing import Any, Dict
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage
from logic.agent import make_graph


class Agent:
    def __init__(self):
        """Initialize the supervisor agent. The graph will be created lazily on first use."""
        self._graph = None
    
    async def _ensure_graph(self):
        """Ensure the graph is initialized (lazy initialization)."""
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
        
        # LangGraph supervisor graph uses SupervisorState
        # thread_id can be passed in the config for state persistence
        config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
        
        # Initialize with messages and next_agent (will be set by supervisor)
        result = await graph.ainvoke(
            {"messages": [HumanMessage(content=user_prompt)], "next_agent": "supervisor"},
            config=config
        )
        
        # Extract the final response from the messages
        if "messages" in result and result["messages"]:
            # Get all assistant/agent messages
            responses = []
            for message in result["messages"]:
                # Skip user messages
                if hasattr(message, "type") and message.type == "human":
                    continue
                    
                content = None
                if hasattr(message, "content"):
                    content = message.content
                elif isinstance(message, dict) and "content" in message:
                    content = message["content"]
                
                if content:
                    responses.append(str(content))
            
            # Return the last meaningful response
            if responses:
                return responses[-1]
        
        return "No response generated."