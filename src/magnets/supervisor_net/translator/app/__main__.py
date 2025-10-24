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
PORT = int(os.getenv("A2A_PORT", "8004"))
A2A_PUBLIC_URL = os.getenv("A2A_PUBLIC_URL", f"http://{HOST}:{PORT}")


def main():
    logger.info("Initializing Translator Agent")

    skills = [
        AgentSkill(
            id="translation_skill",
            name="Language Translation",
            description="Translate text between languages and detect languages using specialized translation agent capabilities.",
            tags=["translation", "language", "multilingual", "localization", "mcp"],
            examples=[
                json.dumps({
                    "type": "text",
                    "content": "Translate 'hello world' to Italian"
                }),
                json.dumps({
                    "type": "text",
                    "content": "What language is 'bonjour' in?"
                }),
                json.dumps({
                    "type": "text",
                    "content": "Translate this text from Spanish to English: 'hola mundo'"
                }),
            ],
        )
    ]

    agent_card = AgentCard(
        protocol_version="0.3.0",
        name="Translator Agent",
        description="A translator agent that can translate any language in any other languange.",
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