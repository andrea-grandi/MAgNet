from typing import Any, Union, Optional


class Tool:
    def __init__(
        self, 
        name: str, 
        docstring: str, 
        model: Any,
        func: Optional[Any] = None
    ) -> None:
        """Initialize a tool with the given parameters."""

        self.name = name
        self.docstring = docstring
        self.model = model
        self.func = func

    # Call the model with the tool's request
    def call(self, request: str):
        r"""{self.docstring}"""

        return self.model.invoke(request).content
    
    # Custom call method to allow passing a function
    def custom_call(self, request: str):
        r"""{self.docstring}"""
        
        return self.func(request) # type: ignore