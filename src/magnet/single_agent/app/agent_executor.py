from typing import Optional, Any, cast
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils.errors import ServerError
from a2a.types import Message, Part, TextPart, Role, InternalError

from app.agent import Agent


class Executor(AgentExecutor):
    def __init__(self):
        self.agent = Agent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        try:
            """Execute the agent with the given context and event queue."""
            
            user_message = self._extract_user_message(context)
            if not user_message:
                raise ValueError("No user message found in request context")
            
            thread_id = context.task_id or "default"
            response = await self.agent.run(user_message, thread_id)
            text_part = TextPart(text=response)
            message = Message(
                message_id="response",
                role=Role.agent,
                parts=cast(list[Part], [text_part])
            )
            
            await event_queue.enqueue_event(message)

        except Exception as e:
            raise ServerError(error=InternalError(message=str(e))) from e
    
    def _extract_user_message(self, context: RequestContext) -> Optional[str]:
        """Extract the user message from the request context."""
        
        message = context.message
        if not message or not message.parts:
            return None
        
        for part in message.parts:
            if isinstance(part, TextPart):
                return part.text
        
        return None
        
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        return