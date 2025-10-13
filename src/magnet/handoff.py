from typing import Optional, List
from langgraph_swarm import create_handoff_tool
from langchain_core.tools import BaseTool


class Handoff:
    def __init__(
        self, 
        agent_name: Optional[str] = None, 
        description: Optional[str] = None
    ) -> None:
        """Initialize a handoff tools."""

        # Recall that the agent name is the name 
        # of the agent to which we are handing off
        self.agent_name = agent_name
        self.description = description

    def create(self, agent_name: str, description: str) -> BaseTool:
        """Build and return the handoff tool using the provided configuration."""

        return create_handoff_tool(
            agent_name=agent_name,
            description=description
        )
    
    def create_multiple(self, agent_name: List[str], description: List[str], num: int) -> List[BaseTool]:
        """Build and return the handoffs list tools using the provided configuration."""

        handoffs = []
        for n in range(num):
            handoffs.append(
                create_handoff_tool(
                    agent_name=f"{agent_name}_{n}",
                    description=description # type: ignore
                )   
            )
            
        return handoffs