"""Context management utilities for tracking net and task execution context using OpenTelemetry baggage."""

from typing import cast

from opentelemetry import baggage

from magnet.utilities.net.models import NetContext


def get_net_context() -> NetContext | None:
    """Get the current net context from OpenTelemetry baggage.

    Returns:
        NetContext instance containing net context information, or None if no context is set
    """
    return cast(NetContext | None, baggage.get_baggage("net_context"))
