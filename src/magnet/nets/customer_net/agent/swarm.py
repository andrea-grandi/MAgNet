from langgraph_swarm import create_swarm
from langgraph.checkpoint.memory import MemorySaver

from .agents import flight_assistant, hotel_assistant, orchestrator


builder = create_swarm(
    agents=[orchestrator, flight_assistant, hotel_assistant], 
    default_active_agent="orchestrator",
)

# Compile with checkpointer
checkpointer = MemorySaver()
app = builder.compile()