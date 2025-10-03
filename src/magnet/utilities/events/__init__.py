"""Backwards compatibility - this module has moved to magnet.events."""

import warnings
from abc import ABC
from collections.abc import Callable
from typing import Any, TypeVar

from typing_extensions import deprecated

import magnet.events as new_events
from magnet.events.base_events import BaseEvent
from magnet.events.event_types import EventTypes

EventT = TypeVar("EventT", bound=BaseEvent)


warnings.warn(
    "Importing from 'magnet.utilities.events' is deprecated and will be removed in v1.0.0. "
    "Please use 'magnet.events' instead.",
    DeprecationWarning,
    stacklevel=2,
)


@deprecated("Use 'from magnet.events import BaseEventListener' instead")
class BaseEventListener(new_events.BaseEventListener, ABC):
    """Deprecated: Use magnet.events.BaseEventListener instead."""


@deprecated("Use 'from magnet.events import magnet_event_bus' instead")
class magnet_event_bus:  # noqa: N801
    """Deprecated: Use magnet.events.magnet_event_bus instead."""

    @classmethod
    def on(
        cls, event_type: type[EventT]
    ) -> Callable[[Callable[[Any, EventT], None]], Callable[[Any, EventT], None]]:
        """Delegate to the actual event bus instance."""
        return new_events.magnet_event_bus.on(event_type)

    @classmethod
    def emit(cls, source: Any, event: BaseEvent) -> None:
        """Delegate to the actual event bus instance."""
        return new_events.magnet_event_bus.emit(source, event)

    @classmethod
    def register_handler(
        cls, event_type: type[EventTypes], handler: Callable[[Any, EventTypes], None]
    ) -> None:
        """Delegate to the actual event bus instance."""
        return new_events.magnet_event_bus.register_handler(event_type, handler)

    @classmethod
    def scoped_handlers(cls) -> Any:
        """Delegate to the actual event bus instance."""
        return new_events.magnet_event_bus.scoped_handlers()


@deprecated("Use 'from magnet.events import NetKickoffStartedEvent' instead")
class NetKickoffStartedEvent(new_events.NetKickoffStartedEvent):
    """Deprecated: Use magnet.events.NetKickoffStartedEvent instead."""


@deprecated("Use 'from magnet.events import NetKickoffCompletedEvent' instead")
class NetKickoffCompletedEvent(new_events.NetKickoffCompletedEvent):
    """Deprecated: Use magnet.events.NetKickoffCompletedEvent instead."""


@deprecated("Use 'from magnet.events import AgentExecutionCompletedEvent' instead")
class AgentExecutionCompletedEvent(new_events.AgentExecutionCompletedEvent):
    """Deprecated: Use magnet.events.AgentExecutionCompletedEvent instead."""


@deprecated("Use 'from magnet.events import MemoryQueryCompletedEvent' instead")
class MemoryQueryCompletedEvent(new_events.MemoryQueryCompletedEvent):
    """Deprecated: Use magnet.events.MemoryQueryCompletedEvent instead."""


@deprecated("Use 'from magnet.events import MemorySaveCompletedEvent' instead")
class MemorySaveCompletedEvent(new_events.MemorySaveCompletedEvent):
    """Deprecated: Use magnet.events.MemorySaveCompletedEvent instead."""


@deprecated("Use 'from magnet.events import MemorySaveStartedEvent' instead")
class MemorySaveStartedEvent(new_events.MemorySaveStartedEvent):
    """Deprecated: Use magnet.events.MemorySaveStartedEvent instead."""


@deprecated("Use 'from magnet.events import MemoryQueryStartedEvent' instead")
class MemoryQueryStartedEvent(new_events.MemoryQueryStartedEvent):
    """Deprecated: Use magnet.events.MemoryQueryStartedEvent instead."""


@deprecated("Use 'from magnet.events import MemoryRetrievalCompletedEvent' instead")
class MemoryRetrievalCompletedEvent(new_events.MemoryRetrievalCompletedEvent):
    """Deprecated: Use magnet.events.MemoryRetrievalCompletedEvent instead."""


@deprecated("Use 'from magnet.events import MemorySaveFailedEvent' instead")
class MemorySaveFailedEvent(new_events.MemorySaveFailedEvent):
    """Deprecated: Use magnet.events.MemorySaveFailedEvent instead."""


@deprecated("Use 'from magnet.events import MemoryQueryFailedEvent' instead")
class MemoryQueryFailedEvent(new_events.MemoryQueryFailedEvent):
    """Deprecated: Use magnet.events.MemoryQueryFailedEvent instead."""


@deprecated("Use 'from magnet.events import KnowledgeRetrievalStartedEvent' instead")
class KnowledgeRetrievalStartedEvent(new_events.KnowledgeRetrievalStartedEvent):
    """Deprecated: Use magnet.events.KnowledgeRetrievalStartedEvent instead."""


@deprecated("Use 'from magnet.events import KnowledgeRetrievalCompletedEvent' instead")
class KnowledgeRetrievalCompletedEvent(new_events.KnowledgeRetrievalCompletedEvent):
    """Deprecated: Use magnet.events.KnowledgeRetrievalCompletedEvent instead."""


@deprecated("Use 'from magnet.events import LLMStreamChunkEvent' instead")
class LLMStreamChunkEvent(new_events.LLMStreamChunkEvent):
    """Deprecated: Use magnet.events.LLMStreamChunkEvent instead."""


__all__ = [
    "AgentExecutionCompletedEvent",
    "BaseEventListener",
    "NetKickoffCompletedEvent",
    "NetKickoffStartedEvent",
    "KnowledgeRetrievalCompletedEvent",
    "KnowledgeRetrievalStartedEvent",
    "LLMStreamChunkEvent",
    "MemoryQueryCompletedEvent",
    "MemoryQueryFailedEvent",
    "MemoryQueryStartedEvent",
    "MemoryRetrievalCompletedEvent",
    "MemorySaveCompletedEvent",
    "MemorySaveFailedEvent",
    "MemorySaveStartedEvent",
    "magnet_event_bus",
]

__deprecated__ = "Use 'magnet.events' instead of 'magnet.utilities.events'"
