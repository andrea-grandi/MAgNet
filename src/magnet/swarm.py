from typing import Any, List, Optional, Union
from langgraph.graph.state import StateGraph, CompiledStateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph_swarm import create_swarm


class Swarm:
    def __init__(
        self, 
        agents: Union[List[CompiledStateGraph], CompiledStateGraph], 
        default_active_agent: str,
    ) -> None:
        """Initialize a swarm with the given parameters."""

        self.agents = agents
        self.default_active_agent = default_active_agent

    def create(self) -> StateGraph:
        """Build and return the swarm using the provided configuration."""

        return create_swarm(
            agents=self.agents, # type: ignore
            default_active_agent=self.default_active_agent
        )
    
    def compile(self) -> CompiledStateGraph:
        """Compile the swarm into a runnable state graph with optional checkpointing."""

        checkpointer = InMemorySaver() # short-term memory
        store = InMemoryStore() # long-term memory

        return self.create().compile(checkpointer=checkpointer, store=store)


