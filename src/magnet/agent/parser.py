from typing import Any, Dict, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agent.models import AgentRequest  

load_dotenv()


class Parser:
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.2):
        llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.llm_with_tools = llm.bind_tools([AgentRequest])
        self.prompt = ChatPromptTemplate.from_messages([ #TODO
            (
                "system", 
                """system prompt text here"""
            ), 
            (
                "human", 
                "{user_prompt}"
            )
        ])

        self.chain = self.prompt | self.llm_with_tools

    async def parse(self, user_prompt: str) -> Optional[Dict[str, Any]]:
        ai_message = await self.chain.ainvoke({"user_prompt": user_prompt, "recursion_limit": 5})

        if not getattr(ai_message, "tool_calls", None):
            return None

        tool_call = ai_message.tool_calls[0]
        if tool_call["name"] != AgentRequest.__name__:
            return None

        args = tool_call["args"] or {}

        if "minutes" not in args or args["minutes"] is None:
            args["minutes"] = 30

        return args