import os
import json
import uvicorn

from dotenv import load_dotenv
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill

from app.agent_executor import Executor
from agent.models import AgentRequest

load_dotenv()

HOST = os.getenv("A2A_HOST")
PORT = int(os.getenv("A2A_PORT")) #type: ignore
A2A_PUBLIC_URL = os.getenv("A2A_PUBLIC_URL")


def main():
    skills = [
        AgentSkill(
            id=AgentRequest.__name__,
            name="Skill name", #TODO
            description="Skill description", #TODO
            tags=["", ""], #TODO
            examples=[json.dumps(AgentRequest.model_json_schema())],
        )
    ]

    agent_card = AgentCard(
        protocol_version="0.3.0",
        name="Agent name", #TODO
        description="Agent description", #TODO
        url=A2A_PUBLIC_URL, #type: ignore
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
    uvicorn.run(main(), host=HOST, port=PORT) #type: ignore