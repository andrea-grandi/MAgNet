from .llm import model
from .state import AgentState


async def model_node(state: AgentState) -> AgentState:
    response = await model.ainvoke({"messages": state["messages"]})

    return {
        "messages": [response],
    }
