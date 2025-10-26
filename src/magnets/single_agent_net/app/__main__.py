import os
import json
import uvicorn

from dotenv import load_dotenv
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill

from app.agent_executor import Executor

load_dotenv()

HOST = os.getenv("A2A_HOST", "localhost")
PORT = int(os.getenv("A2A_PORT", "8001"))
A2A_PUBLIC_URL = os.getenv("A2A_PUBLIC_URL", f"http://{HOST}:{PORT}")


def main():
    skills = [
        AgentSkill(
            id="calculator_skill",
            name="Calculator & Statistics",
            description="Perform arithmetic operations and statistical calculations using MCP tools",
            tags=["math", "calculator", "statistics", "mcp"],
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
                    "content": "Multiply 3 by 12"
                }),
            ],
        )
    ]

    agent_card = AgentCard(
        protocol_version="0.3.0",
        name="MCP Swarm Agent",
        description="A LangGraph agent that uses Model Context Protocol (MCP) tools for mathematical operations",
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