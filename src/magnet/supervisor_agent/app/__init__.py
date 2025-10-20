"""MAgNet Supervisor Agent - Multi-Agent System Application.

This module contains the A2A server application for the supervisor agent
that coordinates specialized agents for math, coding, and translation tasks.
"""

from app.agent import Agent
from app.agent_executor import Executor

__all__ = ["Agent", "Executor"]
