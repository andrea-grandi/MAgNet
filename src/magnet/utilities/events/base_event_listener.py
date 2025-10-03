"""Backwards compatibility stub for magnet.utilities.events.base_event_listener."""

import warnings

from magnet.events import BaseEventListener

warnings.warn(
    "Importing from 'magnet.utilities.events.base_event_listener' is deprecated and will be removed in v1.0.0. "
    "Please use 'from magnet.events import BaseEventListener' instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["BaseEventListener"]
