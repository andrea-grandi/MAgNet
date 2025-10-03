from abc import ABC, abstractmethod

from magnet.events.event_bus import NetAIEventsBus, magnet_event_bus


class BaseEventListener(ABC):
    verbose: bool = False

    def __init__(self):
        super().__init__()
        self.setup_listeners(magnet_event_bus)

    @abstractmethod
    def setup_listeners(self, magnet_event_bus: NetAIEventsBus):
        pass
