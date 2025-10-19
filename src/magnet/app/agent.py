
from agent.graph import graph


class Agent:
    async def run(self, user_prompt: str, thread_id: str) -> str:
        """Run the agent with the given user prompt and thread ID."""
        
        initial_state = {
            "raw_text": user_prompt,
            "thread_id": thread_id
        }

        final_state = await graph.ainvoke(initial_state)

        return final_state.get("final_text", "No response generated.")