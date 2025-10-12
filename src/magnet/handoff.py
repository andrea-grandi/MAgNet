from langgraph_swarm import create_handoff_tool
from langchain_core.tools import BaseTool


class Handoff:
    def __init__(
        self, 
        agent_name: str, 
        description: str
    ) -> None:
        """Initialize a handoff tool with the given parameters."""

        # Recall that the agent name is the name 
        # of the agent to which we are handing off
        self.agent_name = agent_name
        self.description = description

    def create(self) -> BaseTool:
        """Build and return the handoff tool using the provided configuration."""

        return create_handoff_tool(
            agent_name=self.agent_name,
            description=self.description
        )