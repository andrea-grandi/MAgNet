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
        prompt: str,
        tools: Optional[List[Union[Tool, Handoff]]] = None, 
    ) -> None:
        """Initialize an agent with the given parameters."""

        self.name = name
        self.model = model
        self.tools = tools
        self.prompt = prompt

    def create(self, tools: List[Tool]) -> List[CompiledStateGraph]:
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
        
        agents = []
        for n in range(num):
            # Separate handoff tools from normal tools
            handoff_tools = [tool for tool in tools if isinstance(tool, BaseTool)]
            normal_tools = [tool for tool in tools if not isinstance(tool, BaseTool)]
            
            # Filter out self-handoff (agent cannot handoff to itself)
            # This prevents math_agent_0 from having transfer_to_math_agent_0
            filtered_handoff_tools = [
                tool for tool in handoff_tools 
                if tool.name != f"transfer_to_{self.name}_{n}"
            ]
            
            # Combine filtered handoffs with normal tools
            tools_for_agent = filtered_handoff_tools + normal_tools

            agents.append(
                create_react_agent(
                    name=f"{self.name}_{n}",
                    model=self.model,
                    tools=tools_for_agent, # type: ignore
                    prompt=self.prompt.format(num=num) if self.prompt else None
                )
            )

        return agents