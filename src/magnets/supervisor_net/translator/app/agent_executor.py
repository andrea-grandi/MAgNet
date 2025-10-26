import logging

from typing import Optional, Any, cast
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils.errors import ServerError
from a2a.types import Message, Part, TextPart, Role, InternalError

from app.agent import Agent

logger = logging.getLogger(__name__)


class Executor(AgentExecutor):
    def __init__(self):
        self.agent = Agent()
        logger.info("Translator agent executor initialized")

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Execute the translator agent with the given context and event queue.
        
        The translator agent processes translation tasks using MCP tools.
        """
        try:
            
            user_message = self._extract_user_message(context)
            if not user_message:
                raise ValueError("No user message found in request context")
            
            logger.info(f"[A2A] Received request: {user_message[:100]}...")
            logger.info(f"Processing user request: {user_message[:100]}...")
            
            thread_id = context.task_id or "default"
            logger.info(f"[A2A] Thread ID: {thread_id}")
            logger.info(f"Calling agent.run() with thread_id: {thread_id}")
            
            try:
                response = await self.agent.run(user_message, thread_id)
                logger.info(f"Agent.run() completed successfully")
                logger.info(f"[A2A] Response generated: {len(response)} characters")
            except Exception as agent_error:
                logger.error(f"[A2A] Error in agent execution: {str(agent_error)}", exc_info=True)
                logger.error(f"Error in agent.run(): {str(agent_error)}", exc_info=True)
                raise
            
            logger.info(f"Generated response: {response[:100]}...")
            
            text_part = TextPart(text=response)
            message = Message(
                message_id="response",
                role=Role.agent,
                parts=cast(list[Part], [text_part])
            )
            
            logger.info(f"[A2A] Sending response back to client")
            await event_queue.enqueue_event(message)
            logger.info(f"[A2A] Request completed successfully")

        except Exception as e:
            logger.error(f"[A2A] Fatal error in A2A execution: {str(e)}", exc_info=True)
            logger.error(f"Error executing translator agent: {str(e)}", exc_info=True)
            raise ServerError(error=InternalError(message=str(e))) from e
    
    def _extract_user_message(self, context: RequestContext) -> Optional[str]:
        """Extract the user message from the request context."""
        
        message = context.message
        logger.debug(f"[A2A] Parsing message object")
        logger.debug(f"Message object: {message}")
        
        if not message:
            logger.warning("No message in context")
            return None
            
        if not message.parts:
            logger.warning("No parts in message")
            return None
        
        logger.debug(f"Message parts: {message.parts}")
        logger.debug(f"Number of parts: {len(message.parts)}")
        
        for idx, part in enumerate(message.parts):
            logger.debug(f"Processing part {idx}: {part}")
            logger.debug(f"Part type: {type(part)}")
            logger.debug(f"Part repr: {repr(part)}")
            
            if isinstance(part, TextPart):
                text = part.text
                logger.info(f"Extracted text from TextPart directly: {text}")
                return text
            
            if hasattr(part, 'root'):
                logger.debug(f"Part has root: {part.root}")
                logger.debug(f"Root type: {type(part.root)}")
                
                if isinstance(part.root, TextPart):
                    text = part.root.text
                    logger.info(f"Extracted text from Part.root: {text}")
                    return text
            
            if isinstance(part, dict) and 'text' in part:
                text = part['text']
                logger.info(f"Extracted text from dict: {text}")
                return text
        
        logger.warning("No text content found in any message parts")
        return None
        
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        return