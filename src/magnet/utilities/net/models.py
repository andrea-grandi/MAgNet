"""Models for net-related data structures."""

from pydantic import BaseModel, Field


class NetContext(BaseModel):
    """Model representing net context information.

    Attributes:
        id: Unique identifier for the net.
        key: Optional net key/name for identification.
    """

    id: str | None = Field(default=None, description="Unique identifier for the net")
    key: str | None = Field(
        default=None, description="Optional net key/name for identification"
    )
