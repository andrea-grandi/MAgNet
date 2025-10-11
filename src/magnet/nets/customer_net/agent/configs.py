from dataclasses import dataclass, field
from typing import Optional

from .models import AgentRole, MCPClientConfig, AgentMemoryConfig, AgentConfig
from .prompts import (
    ORCHESTRATOR_PROMPT,
    HOTEL_ASSISTANT_PROMPT,
    FLIGHT_ASSISTANT_PROMPT,
)


# MCP Server Configurations
FLIGHT_MCP_CONFIG = MCPClientConfig(
    server_url="http://localhost:8787/mcp",
    server_name="flight_mcp",
    timeout=30,
    max_retries=3,
)

HOTEL_MCP_CONFIG = MCPClientConfig(
    server_url="http://localhost:8989/mcp",
    server_name="hotel_mcp",
    timeout=30,
    max_retries=3,
)


# Agent Configurations
ORCHESTRATOR_CONFIG = AgentConfig(
    name="orchestrator",
    role=AgentRole.ORCHESTRATOR,
    model_name="gpt-4o",
    temperature=0.5,
    max_tokens=4000,
    system_prompt=ORCHESTRATOR_PROMPT,
    tools=[],
    handoff_to=["flight_assistant", "hotel_assistant"],
    memory_config=AgentMemoryConfig(
        enabled=True,
        max_messages=100,
        summary_threshold=30,
    ),
    max_iterations=15,
)

FLIGHT_ASSISTANT_CONFIG = AgentConfig(
    name="flight_assistant",
    role=AgentRole.FLIGHT_ASSISTANT,
    model_name="gpt-4o-mini",
    temperature=0.3,
    max_tokens=8000,
    system_prompt=FLIGHT_ASSISTANT_PROMPT,
    tools=["search_flights"],
    handoff_to=["orchestrator", "hotel_assistant"],
    memory_config=AgentMemoryConfig(
        enabled=True,
        max_messages=80,
        summary_threshold=25,
    ),
    mcp_client=FLIGHT_MCP_CONFIG,
    max_iterations=10,
)

HOTEL_ASSISTANT_CONFIG = AgentConfig(
    name="hotel_assistant",
    role=AgentRole.HOTEL_ASSISTANT,
    model_name="gpt-4o-mini",
    temperature=0.2,
    max_tokens=6000,
    system_prompt=HOTEL_ASSISTANT_PROMPT,
    tools=["search_hotels"],
    handoff_to=["orchestrator", "flight_assistant"],
    memory_config=AgentMemoryConfig(
        enabled=True,
        max_messages=60,
        summary_threshold=20,
    ),
    mcp_client=HOTEL_MCP_CONFIG,
    max_iterations=8,
)


# Swarm Configuration
@dataclass
class SwarmConfig:
    """Configuration for the entire swarm."""

    num_agents: int = 3
    default_agent: str = "orchestrator"
    agents: list[AgentConfig] = field(default_factory=lambda: [
        ORCHESTRATOR_CONFIG,
        FLIGHT_ASSISTANT_CONFIG,
        HOTEL_ASSISTANT_CONFIG,
    ])
    max_swarm_iterations: int = 20
    enable_streaming: bool = True
    enable_checkpointing: bool = True
    checkpoint_dir: str = "./checkpoints"
    
    def get_agent_by_name(self, name: str) -> Optional[AgentConfig]:
        """Get agent configuration by name."""

        for agent in self.agents:
            if agent.name == name:
                return agent
        return None
    
    def get_agent_by_id(self, agent_id: str) -> Optional[AgentConfig]:
        """Get agent configuration by ID."""

        for agent in self.agents:
            if agent.id == agent_id:
                return agent
        return None
    
    def to_dict(self) -> dict:
        return {
            "num_agents": self.num_agents,
            "default_agent": self.default_agent,
            "agents": [agent.to_dict() for agent in self.agents],
            "max_swarm_iterations": self.max_swarm_iterations,
            "enable_streaming": self.enable_streaming,
            "enable_checkpointing": self.enable_checkpointing,
            "checkpoint_dir": self.checkpoint_dir,
        }

# Create default swarm configuration
SWARM_CONFIG = SwarmConfig()
