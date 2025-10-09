import uuid

from typing import List, Optional, Dict, Any, Union, Annotated
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage, BaseMessage
from langchain_core.tools import BaseTool
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseLanguageModel
from langchain.memory import ConversationBufferMemory
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

from base_agent.agent import BaseAgent
from .state import AgentState
from .graph import build_graph


class ChatAgent(BaseAgent):
    """Chat agent LLM."""

    def __init__(
        self,
        model: ChatOpenAI,
        tools: Optional[List[BaseTool]] = None,
        system_prompt: Optional[Union[SystemMessage, str]] = None,
        memory: Optional[ConversationBufferMemory] = None,
        token_limit: Optional[int] = None,
        agent_id: Optional[str] = None,
    ) -> None:
        self.model = model
        self.tools = tools or []
        self.system_prompt = system_prompt
        self.memory = memory or ConversationBufferMemory(return_messages=True)
        self.token_limit = token_limit
        self.agent_id = agent_id if agent_id else str(uuid.uuid4())
        self.terminated = False
        self.graph = build_graph()

        def model_call_node(state: AgentState) -> AgentState:
            messages = state["messages"]
            response = self.model.invoke(f"{[self.system_prompt]} {messages}")
            return {
                "messages": [response],
                "tool_results": state.get("tool_results", []),
                "metadata": state.get("metadata", {}),
                "token_usage": state.get("token_usage", {}),
                "step_count": state.get("step_count", 0)
            }

        def maybe_call_tool(state: AgentState):
            last_msg = state["messages"][-1]
            if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
                return "continue"
            else:
                return "end"
            
    
    def step(self, user_input: Union[BaseMessage, str]) -> str:
        """Executes a single step in the chat session, generating a response to the input message."""

        self.memory.chat_memory.add_message(HumanMessage(content=user_input))

        system_message = SystemMessage(content=f"{self.system_prompt}")

        messages = [system_message]
        messages.extend(self.memory.chat_memory.messages)

        state = {"messages": messages}
        result = self.graph.invoke(state)

        ai_messages = [m for m in result["messages"] if isinstance(m, AIMessage)]
        if not ai_messages:
            return "(no response)"
        response = ai_messages[-1].content

        self.memory.chat_memory.add_message(AIMessage(content=response))
        return response

    def reset(self):
        """Pulisce la memoria dell'agente."""
        self.memory.clear()

