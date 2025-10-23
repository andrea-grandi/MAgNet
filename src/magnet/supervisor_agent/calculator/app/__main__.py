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
PORT = int(os.getenv("A2A_PORT", "8002"))
A2A_PUBLIC_URL = os.getenv("A2A_PUBLIC_URL", f"http://{HOST}:{PORT}")


def main():
    logger.info("Initializing Math Agent")

    skills = [
        AgentSkill(
            id="math_skill",
            name="Mathematics & Statistics",
            description="Perform arithmetic operations and statistical calculations using specialized math agent with MCP calculator tools",
            tags=["math", "calculator", "statistics", "arithmetic", "mcp"],
            examples=[
                json.dumps({
                    "type": "text",
                    "content": "Calculate 15 + 27"
                }),
                json.dumps({
                    "type": "text", 
                    "content": "What is the average of 10, 20, 30, 40, 50?"
                }),
                json.dumps({
                    "type": "text",
                    "content": "Calculate the standard deviation of [5, 10, 15, 20, 25]"
                }),
            ],
        )
    ]

    agent_card = AgentCard(
        protocol_version="0.3.0",
        name="Math Agent",
        description="A math expert that can solve algebra and statistical problems using MCP servers.",
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