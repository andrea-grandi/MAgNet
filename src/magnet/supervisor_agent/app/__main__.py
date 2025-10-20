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
        ),
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
        ),
        AgentSkill(
            id="translation_skill",
            name="Language Translation",
            description="Translate text between languages and detect languages using specialized translation agent with MCP translation tools",
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
        name="MAgNet Supervisor Agent",
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
    print(f"Starting MAgNet Supervisor Agent on {HOST}:{PORT}")
    print(f"Public URL: {A2A_PUBLIC_URL}")
    print(f"Managing 3 specialized agents:")
    print(f"   • Math Agent (Calculator MCP)")
    print(f"   • Coding Agent (Coding MCP)")
    print(f"   • Translation Agent (Translation MCP)")
    uvicorn.run(main(), host=HOST, port=PORT)