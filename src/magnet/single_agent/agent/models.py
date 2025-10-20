from pydantic import BaseModel, Field
from typing import Optional, List


class AgentInput(BaseModel):
    """Model for agent requests."""


class AgentOutput(BaseModel):
    """Model for agent outputs."""