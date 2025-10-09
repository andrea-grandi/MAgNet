import logging
import uuid

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.types import Artifact, TaskArtifactUpdateEvent, Part, TextPart
from langchain_core.messages import HumanMessage

from .agent import ChatAgent 

logger = logging.getLogger(__name__)


class ChatAgentExecutor(AgentExecutor):
    def __init__(self) -> None:
        self.agent = ChatAgent()

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """
        Cancel the current task execution.
        
        Args:
            context: Request context with task information
            event_queue: Queue for publishing cancellation events
        """
        logger.info(f"Cancellation requested for task {context.task_id}")
        # For now, we don't have a way to cancel the LangChain execution
        # In a more complex implementation, you would set a cancellation flag
        pass

    async def execute(
        self, 
        context: RequestContext, 
        event_queue: EventQueue
    ) -> None:
        """
        Execute the chat agent with the given task.
        
        Args:
            context: Request context with task data and metadata
            event_queue: Queue for publishing events and artifacts
        """
        try:
            # Extract user input from message parts
            user_message = ""
            if context.message and context.message.parts:
                for part in context.message.parts:
                    if isinstance(part.root, TextPart):
                        user_message = part.root.text
                        break
            
            if not user_message:
                logger.error("No input message provided")
                return
            
            logger.info(f"Processing user message: {user_message}")
            
            # Create HumanMessage for the agent
            human_message = HumanMessage(content=user_message)
            
            # Create artifact ID for streaming response
            artifact_id = str(uuid.uuid4())
            
            # Stream responses from the agent
            async for chunk in self.agent.stream(human_message):
                content = chunk.get("content", "")
                is_complete = chunk.get("is_task_complete", False)
                
                if content:
                    # Create text part
                    text_part = TextPart(text=content)
                    part = Part(root=text_part)
                    
                    # Create artifact with text part
                    artifact = Artifact(
                        artifact_id=artifact_id,
                        parts=[part]
                    )
                    
                    # Create artifact update event
                    event = TaskArtifactUpdateEvent(
                        task_id=context.task_id or "",
                        context_id=context.context_id or "",
                        artifact=artifact,
                        append=False,
                        last_chunk=is_complete
                    )
                    
                    # Enqueue the event
                    await event_queue.enqueue_event(event)
                    
                    logger.debug(f"Published artifact chunk: {content[:50]}...")
            
            logger.info(f"Chat agent execution completed")
            
        except Exception as e:
            logger.error(f"Error executing chat agent: {e}", exc_info=True)
            raise
