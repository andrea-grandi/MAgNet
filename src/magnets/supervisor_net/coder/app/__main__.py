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
PORT = int(os.getenv("A2A_PORT", "8003"))
A2A_PUBLIC_URL = os.getenv("A2A_PUBLIC_URL", f"http://{HOST}:{PORT}")


def main():
    logger.info("Initializing Coder Agent")

    skills = [
        AgentSkill(
            id="coding_skill",
            name="Code Generation & Review",
            description="Generate code, review code quality, and debug issues using specialized coding agent with MCP coding tools",
            tags=["coding", "programming", "debugging", "code-review", "development", "mcp"],
            examples=[
                json.dumps({
                    "type": "text",
                    "content": "Generate a Python function to calculate fibonacci numbers"
                }),
                json.dumps({
                    "type": "text",
                    "content": "Review this code for quality issues"
                }),
                json.dumps({
                    "type": "text",
                    "content": "Help me debug this Python code with a NameError"
                }),
            ],
        )
    ]

    agent_card = AgentCard(
        protocol_version="0.3.0",
        name="Coder Agent",
        description="A coding specialist that can solve coding problems, data structure problems or algorithm problems, using also a MCP server for helping the coding tasks.",
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