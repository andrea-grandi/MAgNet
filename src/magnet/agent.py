from typing import List, Optional, Any
from langgraph.prebuilt import create_react_agent
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt.chat_agent_executor import Prompt 


class Agent:
    def __init__(
        self, 
        name: str, 
        model: Any, 
        tools: List[Any], 
        prompt: Optional[Prompt] = None
    ) -> None:
        """Initialize an agent with the given parameters."""

        self.name = name
        self.model = model
        self.tools = tools
        self.prompt = prompt

    def create(self) -> CompiledStateGraph:
        """Build and return the agent using the provided configuration."""

        return create_react_agent(
            name=self.name,
            model=self.model,
            tools=self.tools,
            prompt=self.prompt
        )