from typing import List, Optional, Any, Union
from langgraph.prebuilt import create_react_agent
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt.chat_agent_executor import Prompt 
from langchain_core.tools import BaseTool

from magnet.tool import Tool
from magnet.handoff import Handoff


class Agent:
    def __init__(
        self, 
        name: str, 
        model: Any, 
        tools: Optional[List[Union[Tool, Handoff]]] = None, 
        prompt: Optional[Prompt] = None,
    ) -> None:
        """Initialize an agent with the given parameters."""

        self.name = name
        self.model = model
        self.tools = tools
        self.prompt = prompt

    def create(self, tools: List[Union[Tool, Handoff]]) -> List[CompiledStateGraph]:
        """Build and return the agent using the provided configuration."""

        agent = []
        return agent.append(
            create_react_agent(
                name=self.name,
                model=self.model,
                tools=tools, # type: ignore
                prompt=self.prompt
            )
        )

    def create_multiple(self, num: int, tools: List[Union[Tool, Handoff]]) -> List[CompiledStateGraph]:
        """Build and return multiple agent using the provided configuration."""
        
        handoff_tool = []
        for tool in tools:
            if isinstance(tool, BaseTool):
                handoff_tool.append(tool.name.split("_")[-1])

        agents = []
        for n in range(num):
            agents.append(
                create_react_agent(
                    name=f"{self.name}_{n}",
                    model=self.model,
                    tools=tools, # type: ignore
                    prompt=f"""{self.prompt}. 
                            "You are part of a swarm of {num} agents."
                            "You have to talk with other agents in your swarm."""
                )
            )

        return agents