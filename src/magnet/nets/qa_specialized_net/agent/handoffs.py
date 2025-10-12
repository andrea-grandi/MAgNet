from langgraph_swarm import create_handoff_tool


transfer_to_science_router_agent = create_handoff_tool(
    agent_name="science_router_agent",
    description="Transfer user to the science router agent for specialized scientific inquiries.",
)

transfer_to_translator_agent = create_handoff_tool(
    agent_name="translator_agent",
    description="Transfer user to the translator agent for language translation requests.",
)

transfer_to_question_answering_agent = create_handoff_tool(
    agent_name="question_answering_agent",
    description="Transfer user back to the general question answering agent for non-scientific inquiries.",
)

transfer_to_translator_agent = create_handoff_tool(
    agent_name="translator_agent",
    description="Transfer user to the translator agent for language translation requests.",
)

transfer_to_chemistry_agent = create_handoff_tool(
    agent_name="chemistry_agent",
    description="Transfer user to the chemistry agent for chemistry-related questions.",
)

transfer_to_biology_agent = create_handoff_tool(
    agent_name="biology_agent",
    description="Transfer user to the biology agent for biology-related questions.",
)

transfer_to_astronomy_agent = create_handoff_tool(
    agent_name="astronomy_agent",
    description="Transfer user to the astronomy agent for astronomy-related questions.",
)

transfer_to_general_science_agent = create_handoff_tool(
    agent_name="general_science_agent",
    description="Transfer user to the general science agent for interdisciplinary or general scientific questions.",
)

transfer_to_physics_agent = create_handoff_tool(
    agent_name="physics_agent",
    description="Transfer user to the physics agent for physics-related questions.",
)