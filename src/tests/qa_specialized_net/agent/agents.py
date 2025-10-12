
from langgraph.prebuilt import create_react_agent
from .tools import (
    question_answering, 
    translate_text, 
)
from .invoke import invoke_science_swarm
from .llms import GPT_4O_MINI
from .handoffs import (
    transfer_to_science_router_agent,
    transfer_to_translator_agent,
    transfer_to_question_answering_agent,
    transfer_to_translator_agent,
    transfer_to_chemistry_agent,
    transfer_to_biology_agent,
    transfer_to_astronomy_agent,
    transfer_to_general_science_agent,
    transfer_to_physics_agent
)
from .prompts import (
    QUESTION_ANSWERING_PROMPT,
    SCIENCE_ROUTER_PROMPT,
    TRANSLATOR_PROMPT,
    PHYSICS_AGENT_PROMPT,
    CHEMISTRY_AGENT_PROMPT,
    BIOLOGY_AGENT_PROMPT,
    ASTRONOMY_AGENT_PROMPT,
    GENERAL_SCIENCE_AGENT_PROMPT
)
from .configs import (
    QUESTION_ANSWERING_NAME,
    SCIENCE_ROUTER_NAME,
    TRANSLATOR_NAME,
    PHYSICS_NAME,
    CHEMISTRY_NAME,
    BIOLOGY_NAME,
    ASTRONOMY_NAME,
    GENERAL_SCIENCE_NAME
)


# Main three agents
question_answering_agent = create_react_agent(
    name=QUESTION_ANSWERING_NAME,
    model=GPT_4O_MINI,
    tools=[
        question_answering,
        transfer_to_science_router_agent,
        transfer_to_translator_agent
    ],
    prompt=(QUESTION_ANSWERING_PROMPT)
)

science_router_agent = create_react_agent(
    name=SCIENCE_ROUTER_NAME,
    model=GPT_4O_MINI,
    tools=[
        invoke_science_swarm,
        transfer_to_question_answering_agent,
        transfer_to_translator_agent
    ],
    prompt=(SCIENCE_ROUTER_PROMPT)
)

translator_agent = create_react_agent(
    name=TRANSLATOR_NAME,
    model=GPT_4O_MINI,
    tools=[
        translate_text,
        transfer_to_question_answering_agent,
        transfer_to_science_router_agent
    ],
    prompt=(TRANSLATOR_PROMPT)
)


### ===== Specialized Science Agents ===== ###

# 1. Physics Agent
physics_agent = create_react_agent(
    name=PHYSICS_NAME,
    model=GPT_4O_MINI,
    tools=[
        transfer_to_chemistry_agent,
        transfer_to_biology_agent,
        transfer_to_astronomy_agent,
        transfer_to_general_science_agent
    ],
    prompt=(PHYSICS_AGENT_PROMPT)
)

# 2. Chemistry Agent
chemistry_agent = create_react_agent(
    name=CHEMISTRY_NAME,
    model=GPT_4O_MINI,
    tools=[
        transfer_to_physics_agent,
        transfer_to_biology_agent,
        transfer_to_astronomy_agent,
        transfer_to_general_science_agent
    ],
    prompt=(CHEMISTRY_AGENT_PROMPT)
)

# 3. Biology Agent
biology_agent = create_react_agent(
    name=BIOLOGY_NAME,
    model=GPT_4O_MINI,
    tools=[
        transfer_to_physics_agent,
        transfer_to_chemistry_agent,
        transfer_to_astronomy_agent,
        transfer_to_general_science_agent
    ],
    prompt=(BIOLOGY_AGENT_PROMPT)
)

# 4. Astronomy Agent
astronomy_agent = create_react_agent(
    name=ASTRONOMY_NAME,
    model=GPT_4O_MINI,
    tools=[
        transfer_to_physics_agent,
        transfer_to_chemistry_agent,
        transfer_to_biology_agent,
        transfer_to_general_science_agent
    ],
    prompt=(ASTRONOMY_AGENT_PROMPT)
)

# 5. General Science Agent (Coordinator)
general_science_agent = create_react_agent(
    name=GENERAL_SCIENCE_NAME,
    model=GPT_4O_MINI,
    tools=[
        transfer_to_physics_agent,
        transfer_to_chemistry_agent,
        transfer_to_biology_agent,
        transfer_to_astronomy_agent
    ],
    prompt=(GENERAL_SCIENCE_AGENT_PROMPT)
)