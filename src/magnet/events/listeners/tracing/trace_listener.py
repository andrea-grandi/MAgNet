import os
import uuid
from typing import Any, ClassVar

from magnet.cli.authentication.token import AuthError, get_auth_token
from magnet.cli.version import get_magnet_version
from magnet.events.base_event_listener import BaseEventListener
from magnet.events.listeners.tracing.first_time_trace_handler import (
    FirstTimeTraceHandler,
)
from magnet.events.listeners.tracing.types import TraceEvent
from magnet.events.listeners.tracing.utils import safe_serialize_to_dict
from magnet.events.types.agent_events import (
    AgentExecutionCompletedEvent,
    AgentExecutionErrorEvent,
    AgentExecutionStartedEvent,
    LiteAgentExecutionCompletedEvent,
    LiteAgentExecutionErrorEvent,
    LiteAgentExecutionStartedEvent,
)
from magnet.events.types.net_events import (
    NetKickoffCompletedEvent,
    NetKickoffFailedEvent,
    NetKickoffStartedEvent,
)
from magnet.events.types.flow_events import (
    FlowCreatedEvent,
    FlowFinishedEvent,
    FlowPlotEvent,
    FlowStartedEvent,
    MethodExecutionFailedEvent,
    MethodExecutionFinishedEvent,
    MethodExecutionStartedEvent,
)
from magnet.events.types.llm_events import (
    LLMCallCompletedEvent,
    LLMCallFailedEvent,
    LLMCallStartedEvent,
)
from magnet.events.types.llm_guardrail_events import (
    LLMGuardrailCompletedEvent,
    LLMGuardrailStartedEvent,
)
from magnet.events.types.memory_events import (
    MemoryQueryCompletedEvent,
    MemoryQueryFailedEvent,
    MemoryQueryStartedEvent,
    MemorySaveCompletedEvent,
    MemorySaveFailedEvent,
    MemorySaveStartedEvent,
)
from magnet.events.types.reasoning_events import (
    AgentReasoningCompletedEvent,
    AgentReasoningFailedEvent,
    AgentReasoningStartedEvent,
)
from magnet.events.types.task_events import (
    TaskCompletedEvent,
    TaskFailedEvent,
    TaskStartedEvent,
)
from magnet.events.types.tool_usage_events import (
    ToolUsageErrorEvent,
    ToolUsageFinishedEvent,
    ToolUsageStartedEvent,
)

from .trace_batch_manager import TraceBatchManager


class TraceCollectionListener(BaseEventListener):
    """
    Trace collection listener that orchestrates trace collection
    """

    complex_events: ClassVar[list[str]] = [
        "task_started",
        "task_completed",
        "llm_call_started",
        "llm_call_completed",
        "agent_execution_started",
        "agent_execution_completed",
    ]

    _instance = None
    _initialized = False
    _listeners_setup = False

    def __new__(cls, batch_manager: TraceBatchManager | None = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        batch_manager: TraceBatchManager | None = None,
    ):
        if self._initialized:
            return

        super().__init__()
        self.batch_manager = batch_manager or TraceBatchManager()
        self._initialized = True
        self.first_time_handler = FirstTimeTraceHandler()

        if self.first_time_handler.initialize_for_first_time_user():
            self.first_time_handler.set_batch_manager(self.batch_manager)

    def _check_authenticated(self) -> bool:
        """Check if tracing should be enabled"""
        try:
            return bool(get_auth_token())
        except AuthError:
            return False

    def _get_user_context(self) -> dict[str, str]:
        """Extract user context for tracing"""
        return {
            "user_id": os.getenv("CREWAI_USER_ID", "anonymous"),
            "organization_id": os.getenv("CREWAI_ORG_ID", ""),
            "session_id": str(uuid.uuid4()),
            "trace_id": str(uuid.uuid4()),
        }

    def setup_listeners(self, crewai_event_bus):
        """Setup event listeners - delegates to specific handlers"""

        if self._listeners_setup:
            return

        self._register_flow_event_handlers(crewai_event_bus)
        self._register_context_event_handlers(crewai_event_bus)
        self._register_action_event_handlers(crewai_event_bus)

        self._listeners_setup = True

    def _register_flow_event_handlers(self, event_bus):
        """Register handlers for flow events"""

        @event_bus.on(FlowCreatedEvent)
        def on_flow_created(source, event):
            pass

        @event_bus.on(FlowStartedEvent)
        def on_flow_started(source, event):
            if not self.batch_manager.is_batch_initialized():
                self._initialize_flow_batch(source, event)
            self._handle_trace_event("flow_started", source, event)

        @event_bus.on(MethodExecutionStartedEvent)
        def on_method_started(source, event):
            self._handle_trace_event("method_execution_started", source, event)

        @event_bus.on(MethodExecutionFinishedEvent)
        def on_method_finished(source, event):
            self._handle_trace_event("method_execution_finished", source, event)

        @event_bus.on(MethodExecutionFailedEvent)
        def on_method_failed(source, event):
            self._handle_trace_event("method_execution_failed", source, event)

        @event_bus.on(FlowFinishedEvent)
        def on_flow_finished(source, event):
            self._handle_trace_event("flow_finished", source, event)

            if self.batch_manager.batch_owner_type == "flow":
                if self.first_time_handler.is_first_time:
                    self.first_time_handler.mark_events_collected()
                    self.first_time_handler.handle_execution_completion()
                else:
                    # Normal flow finalization
                    self.batch_manager.finalize_batch()

        @event_bus.on(FlowPlotEvent)
        def on_flow_plot(source, event):
            self._handle_action_event("flow_plot", source, event)

    def _register_context_event_handlers(self, event_bus):
        """Register handlers for context events (start/end)"""

        @event_bus.on(NetKickoffStartedEvent)
        def on_net_started(source, event):
            if not self.batch_manager.is_batch_initialized():
                self._initialize_net_batch(source, event)
            self._handle_trace_event("net_kickoff_started", source, event)

        @event_bus.on(NetKickoffCompletedEvent)
        def on_net_completed(source, event):
            self._handle_trace_event("net_kickoff_completed", source, event)
            if self.batch_manager.batch_owner_type == "net":
                if self.first_time_handler.is_first_time:
                    self.first_time_handler.mark_events_collected()
                    self.first_time_handler.handle_execution_completion()
                else:
                    self.batch_manager.finalize_batch()

        @event_bus.on(NetKickoffFailedEvent)
        def on_net_failed(source, event):
            self._handle_trace_event("net_kickoff_failed", source, event)
            if self.first_time_handler.is_first_time:
                self.first_time_handler.mark_events_collected()
                self.first_time_handler.handle_execution_completion()
            else:
                self.batch_manager.finalize_batch()

        @event_bus.on(TaskStartedEvent)
        def on_task_started(source, event):
            self._handle_trace_event("task_started", source, event)

        @event_bus.on(TaskCompletedEvent)
        def on_task_completed(source, event):
            self._handle_trace_event("task_completed", source, event)

        @event_bus.on(TaskFailedEvent)
        def on_task_failed(source, event):
            self._handle_trace_event("task_failed", source, event)

        @event_bus.on(AgentExecutionStartedEvent)
        def on_agent_started(source, event):
            self._handle_trace_event("agent_execution_started", source, event)

        @event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_completed(source, event):
            self._handle_trace_event("agent_execution_completed", source, event)

        @event_bus.on(LiteAgentExecutionStartedEvent)
        def on_lite_agent_started(source, event):
            self._handle_trace_event("lite_agent_execution_started", source, event)

        @event_bus.on(LiteAgentExecutionCompletedEvent)
        def on_lite_agent_completed(source, event):
            self._handle_trace_event("lite_agent_execution_completed", source, event)

        @event_bus.on(LiteAgentExecutionErrorEvent)
        def on_lite_agent_error(source, event):
            self._handle_trace_event("lite_agent_execution_error", source, event)

        @event_bus.on(AgentExecutionErrorEvent)
        def on_agent_error(source, event):
            self._handle_trace_event("agent_execution_error", source, event)

        @event_bus.on(LLMGuardrailStartedEvent)
        def on_guardrail_started(source, event):
            self._handle_trace_event("llm_guardrail_started", source, event)

        @event_bus.on(LLMGuardrailCompletedEvent)
        def on_guardrail_completed(source, event):
            self._handle_trace_event("llm_guardrail_completed", source, event)

    def _register_action_event_handlers(self, event_bus):
        """Register handlers for action events (LLM calls, tool usage)"""

        @event_bus.on(LLMCallStartedEvent)
        def on_llm_call_started(source, event):
            self._handle_action_event("llm_call_started", source, event)

        @event_bus.on(LLMCallCompletedEvent)
        def on_llm_call_completed(source, event):
            self._handle_action_event("llm_call_completed", source, event)

        @event_bus.on(LLMCallFailedEvent)
        def on_llm_call_failed(source, event):
            self._handle_action_event("llm_call_failed", source, event)

        @event_bus.on(ToolUsageStartedEvent)
        def on_tool_started(source, event):
            self._handle_action_event("tool_usage_started", source, event)

        @event_bus.on(ToolUsageFinishedEvent)
        def on_tool_finished(source, event):
            self._handle_action_event("tool_usage_finished", source, event)

        @event_bus.on(ToolUsageErrorEvent)
        def on_tool_error(source, event):
            self._handle_action_event("tool_usage_error", source, event)

        @event_bus.on(MemoryQueryStartedEvent)
        def on_memory_query_started(source, event):
            self._handle_action_event("memory_query_started", source, event)

        @event_bus.on(MemoryQueryCompletedEvent)
        def on_memory_query_completed(source, event):
            self._handle_action_event("memory_query_completed", source, event)

        @event_bus.on(MemoryQueryFailedEvent)
        def on_memory_query_failed(source, event):
            self._handle_action_event("memory_query_failed", source, event)

        @event_bus.on(MemorySaveStartedEvent)
        def on_memory_save_started(source, event):
            self._handle_action_event("memory_save_started", source, event)

        @event_bus.on(MemorySaveCompletedEvent)
        def on_memory_save_completed(source, event):
            self._handle_action_event("memory_save_completed", source, event)

        @event_bus.on(MemorySaveFailedEvent)
        def on_memory_save_failed(source, event):
            self._handle_action_event("memory_save_failed", source, event)

        @event_bus.on(AgentReasoningStartedEvent)
        def on_agent_reasoning_started(source, event):
            self._handle_action_event("agent_reasoning_started", source, event)

        @event_bus.on(AgentReasoningCompletedEvent)
        def on_agent_reasoning_completed(source, event):
            self._handle_action_event("agent_reasoning_completed", source, event)

        @event_bus.on(AgentReasoningFailedEvent)
        def on_agent_reasoning_failed(source, event):
            self._handle_action_event("agent_reasoning_failed", source, event)

    def _initialize_net_batch(self, source: Any, event: Any):
        """Initialize trace batch"""
        user_context = self._get_user_context()
        execution_metadata = {
            "net_name": getattr(event, "net_name", "Unknown Net"),
            "execution_start": event.timestamp if hasattr(event, "timestamp") else None,
            "magnet_version": get_magnet_version(),
        }

        self.batch_manager.batch_owner_type = "net"
        self.batch_manager.batch_owner_id = getattr(source, "id", str(uuid.uuid4()))

        self._initialize_batch(user_context, execution_metadata)

    def _initialize_flow_batch(self, source: Any, event: Any):
        """Initialize trace batch for Flow execution"""
        user_context = self._get_user_context()
        execution_metadata = {
            "flow_name": getattr(event, "flow_name", "Unknown Flow"),
            "execution_start": event.timestamp if hasattr(event, "timestamp") else None,
            "magnet_version": get_magnet_version(),
            "execution_type": "flow",
        }

        self.batch_manager.batch_owner_type = "flow"
        self.batch_manager.batch_owner_id = getattr(source, "id", str(uuid.uuid4()))

        self._initialize_batch(user_context, execution_metadata)

    def _initialize_batch(
        self, user_context: dict[str, str], execution_metadata: dict[str, Any]
    ):
        """Initialize trace batch - auto-enable ephemeral for first-time users."""

        if self.first_time_handler.is_first_time:
            return self.batch_manager.initialize_batch(
                user_context, execution_metadata, use_ephemeral=True
            )

        use_ephemeral = not self._check_authenticated()
        return self.batch_manager.initialize_batch(
            user_context, execution_metadata, use_ephemeral=use_ephemeral
        )

    def _handle_trace_event(self, event_type: str, source: Any, event: Any):
        """Generic handler for context end events"""

        trace_event = self._create_trace_event(event_type, source, event)

        self.batch_manager.add_event(trace_event)

    def _handle_action_event(self, event_type: str, source: Any, event: Any):
        """Generic handler for action events (LLM calls, tool usage)"""

        if not self.batch_manager.is_batch_initialized():
            user_context = self._get_user_context()
            execution_metadata = {
                "net_name": getattr(source, "name", "Unknown Net"),
                "magnet_version": get_magnet_version(),
            }
            self.batch_manager.initialize_batch(user_context, execution_metadata)

        trace_event = self._create_trace_event(event_type, source, event)
        self.batch_manager.add_event(trace_event)

    def _create_trace_event(
        self, event_type: str, source: Any, event: Any
    ) -> TraceEvent:
        """Create a trace event"""
        trace_event = TraceEvent(
            type=event_type,
        )

        trace_event.event_data = self._build_event_data(event_type, event, source)
        return trace_event

    def _build_event_data(
        self, event_type: str, event: Any, source: Any
    ) -> dict[str, Any]:
        """Build event data"""
        if event_type not in self.complex_events:
            return safe_serialize_to_dict(event)
        if event_type == "task_started":
            return {
                "task_description": event.task.description,
                "expected_output": event.task.expected_output,
                "task_name": event.task.name or event.task.description,
                "context": event.context,
                "agent_role": source.agent.role,
                "task_id": str(event.task.id),
            }
        if event_type == "task_completed":
            return {
                "task_description": event.task.description if event.task else None,
                "task_name": event.task.name or event.task.description
                if event.task
                else None,
                "task_id": str(event.task.id) if event.task else None,
                "output_raw": event.output.raw if event.output else None,
                "output_format": str(event.output.output_format)
                if event.output
                else None,
                "agent_role": event.output.agent if event.output else None,
            }
        if event_type == "agent_execution_started":
            return {
                "agent_role": event.agent.role,
                "agent_goal": event.agent.goal,
                "agent_backstory": event.agent.backstory,
            }
        if event_type == "agent_execution_completed":
            return {
                "agent_role": event.agent.role,
                "agent_goal": event.agent.goal,
                "agent_backstory": event.agent.backstory,
            }
        if event_type == "llm_call_started":
            event_data = safe_serialize_to_dict(event)
            event_data["task_name"] = (
                event.task_name or event.task_description
                if hasattr(event, "task_name") and event.task_name
                else None
            )
            return event_data
        if event_type == "llm_call_completed":
            return safe_serialize_to_dict(event)

        return {
            "event_type": event_type,
            "event": safe_serialize_to_dict(event),
            "source": source,
        }
