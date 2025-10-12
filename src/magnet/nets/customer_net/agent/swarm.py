from langgraph_swarm import create_swarm
from langgraph.checkpoint.memory import InMemorySaver

from .agents import flight_assistant, hotel_assistant, orchestrator


builder = create_swarm(
    agents=[orchestrator, flight_assistant, hotel_assistant], 
    default_active_agent="orchestrator",
)

# Compile with checkpointer
checkpointer = InMemorySaver()
app = builder.compile(checkpointer=checkpointer)