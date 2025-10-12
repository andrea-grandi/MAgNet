
from langgraph.checkpoint.memory import InMemorySaver 
from langgraph_swarm import create_swarm

from .agents import (
    question_answering_agent, 
    science_router_agent, 
    translator_agent,
    general_science_agent,
    physics_agent, 
    chemistry_agent,
    biology_agent,
    astronomy_agent
)


# Science swarm with checkpointer
science_swarm_checkpoint = InMemorySaver()
science_swarm = create_swarm(
    agents=[
        general_science_agent,
        physics_agent,
        chemistry_agent,
        biology_agent,
        astronomy_agent
    ],
    default_active_agent="general_science_agent",
)

science_swarm_app = science_swarm.compile(checkpointer=science_swarm_checkpoint)


# Main workflow with checkpointer
checkpoint = InMemorySaver()
workflow = create_swarm(
    agents=[
        question_answering_agent,
        translator_agent,
        science_router_agent
    ],
    default_active_agent="question_answering_agent",
)

app = workflow.compile(checkpointer=checkpoint)