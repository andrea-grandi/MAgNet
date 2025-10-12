"""
Tools that invoke swarms. Separated to avoid circular imports.
"""


def invoke_science_swarm(request: str) -> str:
    """
    Invoke the science swarm to answer scientific questions.
    
    Args:
        request: The scientific question to answer
    
    Returns:
        The answer from the science swarm
    """
    # Import here to avoid circular dependency
    from .swarms import science_swarm_app
    
    config = {"configurable": {"thread_id": f"science_{hash(request)}"}}
    response = science_swarm_app.invoke(
        {"messages": [{"role": "user", "content": request}]},
        config  # type: ignore
    )
    # Extract the final answer from the response
    final_message = response["messages"][-1]
    return final_message.content
