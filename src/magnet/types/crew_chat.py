"""Net chat input models.

This module provides models for defining chat inputs and fields
for net interactions.
"""

from pydantic import BaseModel, Field


class ChatInputField(BaseModel):
    """Represents a single required input for the net.

    Example:
        ```python
        field = ChatInputField(
            name="topic",
            description="The topic to focus on for the conversation"
        )
        ```
    """

    name: str = Field(..., description="The name of the input field")
    description: str = Field(..., description="A short description of the input field")


class ChatInputs(BaseModel):
    """Holds net metadata and input field definitions.

    Example:
        ```python
        inputs = ChatInputs(
            crew_name="topic-based-qa",
            crew_description="Use this net for topic-based Q&A",
            inputs=[
                ChatInputField(name="topic", description="The topic to focus on"),
                ChatInputField(name="username", description="Name of the user"),
            ]
        )
        ```
    """

    crew_name: str = Field(..., description="The name of the net")
    crew_description: str = Field(
        ..., description="A description of the net's purpose"
    )
    inputs: list[ChatInputField] = Field(
        default_factory=list, description="A list of input fields for the net"
    )
