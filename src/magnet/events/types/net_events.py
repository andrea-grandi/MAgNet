from typing import TYPE_CHECKING, Any

from magnet.events.base_events import BaseEvent

if TYPE_CHECKING:
    from magnet.net import Net
else:
    Net = Any


class NetBaseEvent(BaseEvent):
    """Base class for net events with fingerprint handling"""

    net_name: str | None
    net: Net | None = None

    def __init__(self, **data):
        super().__init__(**data)
        self.set_net_fingerprint()

    def set_net_fingerprint(self) -> None:
        if self.net and hasattr(self.net, "fingerprint") and self.net.fingerprint:
            self.source_fingerprint = self.net.fingerprint.uuid_str
            self.source_type = "net"
            if (
                hasattr(self.net.fingerprint, "metadata")
                and self.net.fingerprint.metadata
            ):
                self.fingerprint_metadata = self.net.fingerprint.metadata

    def to_json(self, exclude: set[str] | None = None):
        if exclude is None:
            exclude = set()
        exclude.add("net")
        return super().to_json(exclude=exclude)


class NetKickoffStartedEvent(NetBaseEvent):
    """Event emitted when a net starts execution"""

    inputs: dict[str, Any] | None
    type: str = "net_kickoff_started"


class NetKickoffCompletedEvent(NetBaseEvent):
    """Event emitted when a net completes execution"""

    output: Any
    type: str = "net_kickoff_completed"
    total_tokens: int = 0


class NetKickoffFailedEvent(NetBaseEvent):
    """Event emitted when a net fails to complete execution"""

    error: str
    type: str = "net_kickoff_failed"


class NetTrainStartedEvent(NetBaseEvent):
    """Event emitted when a net starts training"""

    n_iterations: int
    filename: str
    inputs: dict[str, Any] | None
    type: str = "net_train_started"


class NetTrainCompletedEvent(NetBaseEvent):
    """Event emitted when a net completes training"""

    n_iterations: int
    filename: str
    type: str = "net_train_completed"


class NetTrainFailedEvent(NetBaseEvent):
    """Event emitted when a net fails to complete training"""

    error: str
    type: str = "net_train_failed"


class NetTestStartedEvent(NetBaseEvent):
    """Event emitted when a net starts testing"""

    n_iterations: int
    eval_llm: str | Any | None
    inputs: dict[str, Any] | None
    type: str = "net_test_started"


class NetTestCompletedEvent(NetBaseEvent):
    """Event emitted when a net completes testing"""

    type: str = "net_test_completed"


class NetTestFailedEvent(NetBaseEvent):
    """Event emitted when a net fails to complete testing"""

    error: str
    type: str = "net_test_failed"


class NetTestResultEvent(NetBaseEvent):
    """Event emitted when a net test result is available"""

    quality: float
    execution_duration: float
    model: str
    type: str = "net_test_result"
