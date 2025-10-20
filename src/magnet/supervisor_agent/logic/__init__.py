"""MAgNet Supervisor Agent - Logic Layer.

This module contains the core logic for the supervisor agent and its
specialized sub-agents (math, coding, translation).
"""

from logic.agent import make_graph
from logic.math_agent import create_math_agent
from logic.coding_agent import create_coding_agent
from logic.translation_agent import create_translation_agent

__all__ = [
    "make_graph",
    "create_math_agent",
    "create_coding_agent",
    "create_translation_agent",
]
