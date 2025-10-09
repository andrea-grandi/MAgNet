import os
import uvicorn
import uuid
from pathlib import Path

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill
from dotenv import load_dotenv

from .agent_executor import ChatAgentExecutor

load_dotenv()  

host = os.getenv("A2A_HOST")
port = os.getenv("A2A_PORT", 8000)
a2a_public_url = os.getenv("A2A_PUBLIC_URL", f"http://{host}:{port}")


def main():

    skills = [
        AgentSkill(
                id=str(uuid.uuid4()),
                name="Chatting",
                description="Simple chatting.",
                tags=["chat", "greeting"],
            )
    ]

    agent_card = AgentCard(
        protocol_version="0.3.0",
        name="Chat Agent",
        description="A2A Agent for chat.",
        url=a2a_public_url,
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True, push_notifications=False),
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=skills
    )

    http_handler = DefaultRequestHandler(
        agent_executor=ChatAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    app = A2AStarletteApplication(agent_card=agent_card, http_handler=http_handler)
    return app.build()


if __name__ == "__main__":
    uvicorn.run(main(), host=f"{host}", port=int(port))