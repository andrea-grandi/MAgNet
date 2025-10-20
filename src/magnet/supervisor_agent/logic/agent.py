"""Supervisor Agent with Multi-Agent System Architecture."""

import os
from typing import Literal, Annotated
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
from langchain_core.messages import HumanMessage, SystemMessage

from .math_agent import create_math_agent
from .coding_agent import create_coding_agent
from .translation_agent import create_translation_agent

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

model = ChatOpenAI(name="gpt-4o-mini")


# Define the state for the supervisor
class SupervisorState(MessagesState):
    """State for the supervisor agent with routing information."""
    next_agent: str


async def supervisor_node(state: SupervisorState):
    """Supervisor that routes requests to specialized agents."""
    
    messages = state["messages"]
    
    # Check if we already have an agent response (not just user message)
    # If the last message is from an agent/assistant, the task is complete
    if len(messages) > 1:
        last_message = messages[-1]
        # Check if last message is from an agent (has tool calls or is assistant message)
        if hasattr(last_message, 'type') and last_message.type in ['ai', 'assistant']:
            return {"next_agent": "finish"}
    
    # System message for the supervisor
    system_message = SystemMessage(content="""You are a supervisor agent that coordinates three specialized agents:

1. MATH_AGENT: Handles mathematical operations, calculations, arithmetic, and statistics
2. CODING_AGENT: Handles code generation, code review, debugging, and programming tasks
3. TRANSLATION_AGENT: Handles text translation, language detection, and multilingual tasks

Analyze the user's request and decide which agent should handle it.
Only respond with ONE of these exact words: MATH_AGENT, CODING_AGENT, TRANSLATION_AGENT
""")
    
    # Ask the LLM to route the request
    response = await model.ainvoke([system_message] + messages)
    
    # Parse the response to determine routing
    content = str(response.content).upper() if response.content else ""
    
    if "MATH_AGENT" in content or "MATH" in content or "CALCULATION" in content or "CALCULATE" in content:
        next_agent = "math_agent"
    elif "CODING_AGENT" in content or "CODING" in content or "CODE" in content:
        next_agent = "coding_agent"
    elif "TRANSLATION_AGENT" in content or "TRANSLATION" in content or "TRANSLATE" in content:
        next_agent = "translation_agent"
    else:
        # Default to finish if unclear
        next_agent = "finish"
    
    # Don't add supervisor's routing decision to messages
    return {"next_agent": next_agent}


async def math_agent_node(state: SupervisorState):
    """Math agent node that handles mathematical tasks."""
    
    agent = await create_math_agent()
    result = await agent.ainvoke(state)
    
    # Return to supervisor after processing
    return {
        "messages": result["messages"],
        "next_agent": "supervisor"
    }


async def coding_agent_node(state: SupervisorState):
    """Coding agent node that handles programming tasks."""

    agent = await create_coding_agent()
    result = await agent.ainvoke(state)
    
    # Return to supervisor after processing
    return {
        "messages": result["messages"],
        "next_agent": "supervisor"
    }


async def translation_agent_node(state: SupervisorState):
    """Translation agent node that handles language tasks."""
    
    agent = await create_translation_agent()
    result = await agent.ainvoke(state)
    
    # Return to supervisor after processing
    return {
        "messages": result["messages"],
        "next_agent": "supervisor"
    }


def route_after_supervisor(state: SupervisorState) -> Literal["math_agent", "coding_agent", "translation_agent", "__end__"]:
    """Route to the appropriate agent based on supervisor decision."""
    
    next_agent = state.get("next_agent", "finish")
    
    if next_agent == "math_agent":
        return "math_agent"
    elif next_agent == "coding_agent":
        return "coding_agent"
    elif next_agent == "translation_agent":
        return "translation_agent"
    else:
        return "__end__"


def route_from_agent(state: SupervisorState) -> Literal["supervisor"]:
    """Always return to supervisor after agent completes."""
    return "supervisor"


async def make_graph():
    """Factory function to create the supervisor multi-agent graph."""
    
    # Create the graph
    workflow = StateGraph(SupervisorState)
    
    # Add nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("math_agent", math_agent_node)
    workflow.add_node("coding_agent", coding_agent_node)
    workflow.add_node("translation_agent", translation_agent_node)
    
    # Add edges
    # Start with supervisor
    workflow.add_edge(START, "supervisor")
    
    # Supervisor routes to agents or finishes
    workflow.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "math_agent": "math_agent",
            "coding_agent": "coding_agent",
            "translation_agent": "translation_agent",
            "__end__": END
        }
    )
    
    # Agents return to supervisor
    workflow.add_conditional_edges("math_agent", route_from_agent)
    workflow.add_conditional_edges("coding_agent", route_from_agent)
    workflow.add_conditional_edges("translation_agent", route_from_agent)
    
    # Compile the graph
    graph = workflow.compile()
    
    return graph

