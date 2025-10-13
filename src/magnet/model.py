from typing import Optional
from langchain_openai import ChatOpenAI


class Model:
    def __init__(
        self,
        name: str,
        temperature: Optional[float] = 0.0,
        description: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        """Initialize the model (llm)."""
        
        self.name = name
        self.description = description
        self.version = version
        self.temperature = temperature
    
    def gpt_4o_mini(self) -> ChatOpenAI:
        return ChatOpenAI(model=self.name, temperature=self.temperature)