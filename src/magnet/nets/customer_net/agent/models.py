import uuid

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


class LLMs(Enum):
    """Enum for supported LLM models."""
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_3_5_TURBO = "gpt-3.5-turbo"


class AgentRole(Enum):
    """Enum for agent roles in the flight and hotel swarm."""
    ORCHESTRATOR = "orchestrator"
    HOTEL_ASSISTANT = "hotel_assistant"
    FLIGHT_ASSISTANT = "flight_assistant"


class FlightSearchInput(BaseModel):
    """Input schema for flight search tool."""
    
    city: str = Field(description="The destination city to search flights for")
    date: str = Field(description="The date for the flight in YYYY-MM-DD format")
    time: Optional[str] = Field(default=None, description="Optional time for the flight")
    include_details: bool = Field(default=False, description="Whether to include detailed flight information")


class HotelSearchInput(BaseModel):
    """Input schema for hotel search tool."""
    location: str = Field(description="The location to search hotels in")
    check_in: str = Field(description="Check-in date in YYYY-MM-DD format")
    check_out: str = Field(description="Check-out date in YYYY-MM-DD format")
    guests: int = Field(default=1, description="Number of guests")



@dataclass
class MCPClientConfig:
    """Configuration for MCP (Model Context Protocol) client."""

    server_url: str
    server_name: str
    api_key: Optional[str] = None
    timeout: float = 30.0
    max_retries: int = 3
    
    def to_dict(self) -> dict:
        return {
            "server_url": self.server_url,
            "server_name": self.server_name,
            "api_key": self.api_key,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
        }


@dataclass
class AgentMemoryConfig:
    """Configuration for agent memory."""

    enabled: bool = True
    max_messages: int = 50
    summary_threshold: int = 20
    persistence_enabled: bool = False
    storage_path: Optional[str] = None


@dataclass
class AgentConfig:
    """Configuration for a single agent in the swarm."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    role: AgentRole = AgentRole.ORCHESTRATOR
    model_name: str = LLMs.GPT_4O_MINI.value
    temperature: float = 0.7
    max_tokens: int = 4000
    system_prompt: str = ""
    tools: list[str] = field(default_factory=list)
    handoff_to: list[str] = field(default_factory=list)
    memory_config: AgentMemoryConfig = field(default_factory=AgentMemoryConfig)
    mcp_client: Optional[MCPClientConfig] = None
    max_iterations: int = 10
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.value,
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "system_prompt": self.system_prompt,
            "tools": self.tools,
            "handoff_to": self.handoff_to,
            "memory_config": self.memory_config.__dict__,
            "mcp_client": self.mcp_client.to_dict() if self.mcp_client else None,
            "max_iterations": self.max_iterations,
        }