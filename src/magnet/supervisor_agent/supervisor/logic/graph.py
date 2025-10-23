import os
import json
import asyncio
from functools import partial

from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from logic.client import A2AClient
from .model import get_model

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

SUPERVISOR_MODEL = os.getenv("SUPERVISOR_MODEL", "gpt-4o-mini")
CALCULATOR_A2A_URL = os.getenv("CALCULATOR_A2A_URL")
CODER_A2A_URL = os.getenv("CODER_A2A_URL")
TRANSLATOR_A2A_URL = os.getenv("TRANSLATOR_A2A_URL")

AGENT_URLS = {
    "calculator": CALCULATOR_A2A_URL,
    "coder": CODER_A2A_URL,
    "translator": TRANSLATOR_A2A_URL,
}


async def get_all_agent_cards():
    """Fetch agent cards from all configured specialist agents."""
    cards = {}
    
    async def fetch_card(name, url):
        if not url:
            print(f"[SUPERVISOR] URL for agent {name} is not configured. Skipping.")
            return None
        try:
            async with A2AClient(agent_url=url, agent_name=name) as client:
                card = await client.get_agent_card()
                if card:
                    print(f"[SUPERVISOR] Fetched agent card for {name}")
                    return card
                else:
                    print(f"[SUPERVISOR] Could not fetch agent card for {name}")
                    return None
        except Exception as e:
            print(f"[SUPERVISOR] Error fetching agent card for {name}: {e}")
            return None

    tasks = [fetch_card(name, url) for name, url in AGENT_URLS.items()]
    results = await asyncio.gather(*tasks)

    for name, card in zip(AGENT_URLS.keys(), results):
        if card:
            cards[name] = card
            
    return cards

async def create_supervisor_agent(model_name: str):
    """Create a supervisor specialized agent with supervisor MCP tools."""

    model = get_model(model_name)
    
    agent_cards = await get_all_agent_cards()
    if not agent_cards:
        print("[SUPERVISOR] No agent cards found. The supervisor will have no tools.")
        tools = []
    else:
        print(f"[SUPERVISOR] Found {len(agent_cards)} agent cards.")
        
        @tool
        async def delegate_task(agent_name: str, task_description: str) -> str:
            """Delegate a task to a specific agent. 
            
            Args:
                agent_name: The name of the agent to delegate the task to. Must be one of {list(agent_cards.keys())}.
                task_description: A detailed description of the task for the agent.
            
            Returns:
                The result from the specialist agent.
            """
            agent_url = AGENT_URLS.get(agent_name)
            if not agent_url:
                return f"Error: Agent '{agent_name}' not found. Available agents: {list(agent_cards.keys())}"
            
            try:
                async with A2AClient(agent_url=agent_url, agent_name=agent_name) as client:
                    response = await client.send_message(task_description)
                    return f"Response from {agent_name}: {response}"
            except Exception as e:
                return f"Error communicating with {agent_name}: {e}"

        tools = [delegate_task]

    system_prompt = f"""You are a supervisor agent. Your role is to coordinate a team of specialist agents to solve a user's request.

IMPORTANT: You CANNOT solve tasks yourself. You MUST delegate ALL tasks to specialist agents using the delegate_task tool.

Here are the agents available to you:
{json.dumps(agent_cards, indent=2)}

Workflow:
1. Analyze the user's request
2. Elaborate a plan based on the user query and the agent cards that you have discovered.
3. Identify which specialist agent or agents are best suited for the task.
4. IMMEDIATELY use the delegate_task tool to send the task to those agents (it can be only one or multiple).
5. Wait for the response.
6. Return the response to the user.

DO NOT try to solve the task yourself. ALWAYS use delegate_task.

Available agents:
- calculator: For mathematical calculations and arithmetic operations
- coder: For writing, debugging, or explaining code
- translator: For translating text between languages

Example:
User: "What is 5 + 3?"
You should immediately call: delegate_task(agent_name="calculator", task_description="Calculate 5 + 3")
"""

    agent = create_react_agent(model=model, tools=tools, prompt=system_prompt)
    
    return agent


async def make_graph():
    """Factory function to create the supervisor agent graph.

    This creates a LangGraph ReAct agent.
    The agent can handle text translation, language detection, and multilingual tasks.
    """

    print(f"[SUPERVISOR] Initializing supervisor agent with model: {SUPERVISOR_MODEL}")
    graph = await create_supervisor_agent(SUPERVISOR_MODEL)
    print(f"[SUPERVISOR] Supervisor agent graph initialized successfully")

    return graph
