"""Backwards compatibility stub for magnet.utilities.events.magnet_event_bus."""

import warnings

from magnet.events import magnet_event_bus

warnings.warn(
    "Importing from 'magnet.utilities.events.magnet_event_bus' is deprecated and will be removed in v1.0.0. "
    "Please use 'from magnet.events import magnet_event_bus' instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["magnet_event_bus"]
