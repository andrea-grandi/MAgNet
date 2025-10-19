from typing import Optional, Any
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils.errors import ServerError
from a2a.types import Message, Part, InternalError
from app.agent import Agent


class Executor(AgentExecutor):
    def __init__(self):
        self.agent = Agent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        try:
            """Execute the agent with the given context and event queue."""
            #TODO
            pass

        except Exception as e:
            raise ServerError(error=InternalError(message=str(e))) from e
        
    async def cancel(self, context: RequestContext) -> None:
        return