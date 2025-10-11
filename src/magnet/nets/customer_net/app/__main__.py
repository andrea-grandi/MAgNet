import os
import json
import uvicorn

from dotenv import load_dotenv
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill

from .agent_executor import AgentExecutor

load_dotenv()

HOST = os.getenv("A2A_HOST")
PORT = int(os.getenv("A2A_PORT")) # type: ignore
A2A_PUBLIC_URL = os.getenv("A2A_PUBLIC_URL")


def create_app():
    card = AgentCard(
        protocol_version="0.3.0",
        name="Weather Agent",
        description="Agente A2A de previsão do tempo para corridas de Fórmula 1.",
        url=A2A_PUBLIC_URL, # type: ignore
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True, push_notifications=False),
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=[
            AgentSkill(
                id=AgentRequest.__name__,
                name="Minutely Nowcast",
                description="Retorna previsão minuto a minuto.",
                tags=["weather", "nowcast"],
                examples=[json.dumps(AgentRequest.model_json_schema())],
            )
        ],
    )

    handler = DefaultRequestHandler(
        agent_executor=AgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    a2a_app = A2AStarletteApplication(agent_card=card, http_handler=handler)
    return a2a_app.build()


if __name__ == "__main__":
    uvicorn.run(create_app(), host=HOST, port=PORT) # type: ignore