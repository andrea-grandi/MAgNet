import os
import json
import uvicorn
import logging

from dotenv import load_dotenv
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill

from app.agent_executor import Executor

load_dotenv()

logger = logging.getLogger(__name__)

HOST = os.getenv("A2A_HOST", "localhost")
PORT = int(os.getenv("A2A_PORT", "8001"))
A2A_PUBLIC_URL = os.getenv("A2A_PUBLIC_URL", f"http://{HOST}:{PORT}")


def main():
    logger.info("Initializing Supervisor Agent")

    skills = [
         AgentSkill(
            id="supervisor_skill",
            name="Management and Coordination",
            description="Coordinate other agents in the network to perform the task with a plan. Delegate to other agents for specialized skills.",
            tags=["management", "coordination", "delegation", "paln"],
            examples=[
                json.dumps({
                    "type": "text",
                    "content": "First of all, I make a plan to solve the user request..."
                }),
                json.dumps({
                    "type": "text",
                    "content": "The problem is a translation task, I will ask the translator to perform this task..."
                }),
                json.dumps({
                    "type": "text",
                    "content": "Ok, I have the final answer after checking and managing all the execution path for all the agents..."
                }),
            ],
        ),
    ]

    agent_card = AgentCard(
        protocol_version="0.3.0",
        name="Supervisor Agent",
        description="A multi-agent supervisor that coordinates specialized agents (Math, Coding, Translation) using LangGraph and Model Context Protocol (MCP)",
        url=A2A_PUBLIC_URL,
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True, push_notifications=False),
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=skills
    )

    http_handler = DefaultRequestHandler(
        agent_executor=Executor(),
        task_store=InMemoryTaskStore(),
    )

    a2a_app = A2AStarletteApplication(agent_card=agent_card, http_handler=http_handler)

    return a2a_app.build()


if __name__ == "__main__":
    uvicorn.run(main(), host=HOST, port=PORT)