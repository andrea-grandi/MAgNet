from pydantic import BaseModel, Field
from typing import Optional, List

#TODO
class AgentRequest(BaseModel):
    """Model for agent requests."""


class AgentOutput(BaseModel):
    """Model for agent outputs."""