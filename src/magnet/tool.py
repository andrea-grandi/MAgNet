from typing import Any, Union


class Tool:
    def __init__(
        self, 
        name: str, 
        docstring: str, 
        model: Any,
        request: str
    ) -> None:
        """Initialize a tool with the given parameters."""

        self.name = name
        self.docstring = docstring
        self.model = model
        self.request = request

    # Call the model with the tool's request
    def call(self) -> Union[str, list[Union[str, dict]]]:
        f"""{self.docstring}"""

        response = self.model.invoke(self.request)
        return response.content
    
    # Custom call method to allow passing a function
    def custom_call(self, func: Any) -> Any:
        f"""{self.docstring}"""
        
        return func(self.request)