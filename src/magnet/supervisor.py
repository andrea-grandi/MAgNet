from typing import Any, List, Optional, Union
from langgraph.graph.state import StateGraph, CompiledStateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph_supervisor import create_supervisor


class Supervisor:
    def __init__(
        self, 
        model: str,
        prompt: str,
        agents: Union[List[CompiledStateGraph], CompiledStateGraph], 
        default_active_agent: str,
    ) -> None:
        """Initialize a supervisor with the given parameters."""

        self.agents = agents
        self.model = model
        self.prompt = prompt

    def create(self) -> StateGraph:
        """Build and return the supervisor using the provided configuration."""

        return create_supervisor(
            agents=self.agents, # type: ignore
            model=self.model, # type: ignore
            prompt=self.prompt
        )
    
    def compile(self) -> CompiledStateGraph:
        """Compile the supervisor into a runnable state graph with optional checkpointing."""

        checkpointer = InMemorySaver() # short-term memory
        store = InMemoryStore() # long-term memory

        return self.create().compile(checkpointer=checkpointer, store=store)

