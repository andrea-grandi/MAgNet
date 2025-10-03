"""NetAI events system for monitoring and extending agent behavior.

This module provides the event infrastructure that allows users to:
- Monitor agent, task, and net execution
- Track memory operations and performance
- Build custom logging and analytics
- Extend NetAI with custom event handlers
"""

from magnet.events.base_event_listener import BaseEventListener
from magnet.events.event_bus import magnet_event_bus
from magnet.events.types.agent_events import (
    AgentEvaluationCompletedEvent,
    AgentEvaluationFailedEvent,
    AgentEvaluationStartedEvent,
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
    NetTestCompletedEvent,
    NetTestFailedEvent,
    NetTestResultEvent,
    NetTestStartedEvent,
    NetTrainCompletedEvent,
    NetTrainFailedEvent,
    NetTrainStartedEvent,
)
from magnet.events.types.flow_events import (
    FlowCreatedEvent,
    FlowEvent,
    FlowFinishedEvent,
    FlowPlotEvent,
    FlowStartedEvent,
    MethodExecutionFailedEvent,
    MethodExecutionFinishedEvent,
    MethodExecutionStartedEvent,
)
from magnet.events.types.knowledge_events import (
    KnowledgeQueryCompletedEvent,
    KnowledgeQueryFailedEvent,
    KnowledgeQueryStartedEvent,
    KnowledgeRetrievalCompletedEvent,
    KnowledgeRetrievalStartedEvent,
    KnowledgeSearchQueryFailedEvent,
)
from magnet.events.types.llm_events import (
    LLMCallCompletedEvent,
    LLMCallFailedEvent,
    LLMCallStartedEvent,
    LLMStreamChunkEvent,
)
from magnet.events.types.llm_guardrail_events import (
    LLMGuardrailCompletedEvent,
    LLMGuardrailStartedEvent,
)
from magnet.events.types.logging_events import (
    AgentLogsExecutionEvent,
    AgentLogsStartedEvent,
)
from magnet.events.types.memory_events import (
    MemoryQueryCompletedEvent,
    MemoryQueryFailedEvent,
    MemoryQueryStartedEvent,
    MemoryRetrievalCompletedEvent,
    MemoryRetrievalStartedEvent,
    MemorySaveCompletedEvent,
    MemorySaveFailedEvent,
    MemorySaveStartedEvent,
)
from magnet.events.types.reasoning_events import (
    AgentReasoningCompletedEvent,
    AgentReasoningFailedEvent,
    AgentReasoningStartedEvent,
    ReasoningEvent,
)
from magnet.events.types.task_events import (
    TaskCompletedEvent,
    TaskEvaluationEvent,
    TaskFailedEvent,
    TaskStartedEvent,
)
from magnet.events.types.tool_usage_events import (
    ToolExecutionErrorEvent,
    ToolSelectionErrorEvent,
    ToolUsageErrorEvent,
    ToolUsageEvent,
    ToolUsageFinishedEvent,
    ToolUsageStartedEvent,
    ToolValidateInputErrorEvent,
)

__all__ = [
    "AgentEvaluationCompletedEvent",
    "AgentEvaluationFailedEvent",
    "AgentEvaluationStartedEvent",
    "AgentExecutionCompletedEvent",
    "AgentExecutionErrorEvent",
    "AgentExecutionStartedEvent",
    "AgentLogsExecutionEvent",
    "AgentLogsStartedEvent",
    "AgentReasoningCompletedEvent",
    "AgentReasoningFailedEvent",
    "AgentReasoningStartedEvent",
    "BaseEventListener",
    "NetKickoffCompletedEvent",
    "NetKickoffFailedEvent",
    "NetKickoffStartedEvent",
    "NetTestCompletedEvent",
    "NetTestFailedEvent",
    "NetTestResultEvent",
    "NetTestStartedEvent",
    "NetTrainCompletedEvent",
    "NetTrainFailedEvent",
    "NetTrainStartedEvent",
    "FlowCreatedEvent",
    "FlowEvent",
    "FlowFinishedEvent",
    "FlowPlotEvent",
    "FlowStartedEvent",
    "KnowledgeQueryCompletedEvent",
    "KnowledgeQueryFailedEvent",
    "KnowledgeQueryStartedEvent",
    "KnowledgeRetrievalCompletedEvent",
    "KnowledgeRetrievalStartedEvent",
    "KnowledgeSearchQueryFailedEvent",
    "LLMCallCompletedEvent",
    "LLMCallFailedEvent",
    "LLMCallStartedEvent",
    "LLMGuardrailCompletedEvent",
    "LLMGuardrailStartedEvent",
    "LLMStreamChunkEvent",
    "LiteAgentExecutionCompletedEvent",
    "LiteAgentExecutionErrorEvent",
    "LiteAgentExecutionStartedEvent",
    "MemoryQueryCompletedEvent",
    "MemoryQueryFailedEvent",
    "MemoryQueryStartedEvent",
    "MemoryRetrievalCompletedEvent",
    "MemoryRetrievalStartedEvent",
    "MemorySaveCompletedEvent",
    "MemorySaveFailedEvent",
    "MemorySaveStartedEvent",
    "MethodExecutionFailedEvent",
    "MethodExecutionFinishedEvent",
    "MethodExecutionStartedEvent",
    "ReasoningEvent",
    "TaskCompletedEvent",
    "TaskEvaluationEvent",
    "TaskFailedEvent",
    "TaskStartedEvent",
    "ToolExecutionErrorEvent",
    "ToolSelectionErrorEvent",
    "ToolUsageErrorEvent",
    "ToolUsageEvent",
    "ToolUsageFinishedEvent",
    "ToolUsageStartedEvent",
    "ToolValidateInputErrorEvent",
    "magnet_event_bus",
]
