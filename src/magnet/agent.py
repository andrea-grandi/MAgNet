"""
LangGraph-based multi-agent system implementation.
This module provides a LangGraph implementation of the multi-agent system
that maintains compatibility with the existing test infrastructure.
"""

from typing import TypedDict, List, Dict, Any, Annotated
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI
import os


class AgentState(TypedDict):
    """State shared across all agents in the graph."""
    question: str
    question_type: str
    agent_responses: Annotated[List[str], operator.add]
    agent_answers: Annotated[List[str], operator.add]
    final_answer: str
    total_prompt_tokens: int
    total_completion_tokens: int
    ground_truth: str
    question_data: Dict[str, Any]


class LangGraphAgent:
    """Individual agent node in the LangGraph."""
    
    def __init__(self, agent_id: int, model_type: str, ans_parser, 
                 question_type: str, temperature: float = 1.0, top_p: float = 1.0):
        self.agent_id = agent_id
        self.model_type = model_type
        self.question_type = question_type
        self.ans_parser = ans_parser
        self.temperature = temperature
        self.top_p = top_p
        
        # Initialize the LLM
        if model_type.startswith("gpt"):
            self.llm = AzureChatOpenAI(
                deployment_name=model_type,
                openai_api_key=os.getenv('OPENAI_KEY'),
                azure_endpoint=os.getenv('OPENAI_IP'),
                api_version='2023-05-15',
                temperature=temperature,
                model_kwargs={"top_p": top_p}
            )
        else:
            # For open-source models, you might need a different setup
            # This is a placeholder - adjust based on your needs
            from langchain_community.llms import VLLMOpenAI
            self.llm = VLLMOpenAI(
                openai_api_key="EMPTY",
                openai_api_base=os.getenv('LLM_IP'),
                model_name=model_type,
                temperature=temperature,
                top_p=top_p
            )
    
    def __call__(self, state: AgentState) -> AgentState:
        """Execute this agent's reasoning step."""
        print(f"Agent {self.agent_id} processing", flush=True)
        
        # Get system prompt based on question type
        sys_prompt = self._get_system_prompt(state["question_type"])
        
        # Construct messages
        messages = []
        if sys_prompt:
            messages.append(SystemMessage(content=sys_prompt))
        
        # Add the question
        from prompt_lib import construct_message
        user_message = construct_message(state["question"], state["question_type"])
        messages.append(HumanMessage(content=user_message["content"]))
        
        # Get response from LLM
        response = self.llm.invoke(messages)
        
        # Parse the answer
        answer, _ = self.ans_parser(response.content, state["question"])
        
        # Update state
        return {
            "agent_responses": [response.content],
            "agent_answers": [answer if answer else ""],
            "total_prompt_tokens": state.get("total_prompt_tokens", 0) + (response.response_metadata.get("token_usage", {}).get("prompt_tokens", 0) if hasattr(response, 'response_metadata') else 0),
            "total_completion_tokens": state.get("total_completion_tokens", 0) + (response.response_metadata.get("token_usage", {}).get("completion_tokens", 0) if hasattr(response, 'response_metadata') else 0),
        }
    
    def _get_system_prompt(self, question_type: str) -> str:
        """Get system prompt based on question type."""
        # You can import from prompt_lib if needed
        prompts = {
            "code_completion": "",
            "mmlu": "",
            "math": "",
            "chess": "",
            "gsm": "",
            "istask": "",
            "sstask": ""
        }
        return prompts.get(question_type, "")


class LangGraphMultiAgent:
    """LangGraph-based multi-agent system with majority voting."""
    
    def __init__(self, agents_num: int, model_type: str, ans_parser, 
                 question_type: str, final_answer_fn, nums: int = 1, 
                 temperature: float = 1.0, top_p: float = 1.0):
        self.agents_num = agents_num
        self.model_type = model_type
        self.ans_parser = ans_parser
        self.question_type = question_type
        self.final_answer_fn = final_answer_fn
        self.temperature = temperature
        self.top_p = top_p
        
        # Build the graph
        self.graph = self._build_graph()
        self.app = self.graph.compile()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add agent nodes
        for i in range(self.agents_num):
            agent = LangGraphAgent(
                agent_id=i,
                model_type=self.model_type,
                ans_parser=self.ans_parser,
                question_type=self.question_type,
                temperature=self.temperature,
                top_p=self.top_p
            )
            workflow.add_node(f"agent_{i}", agent)
        
        # Add aggregator node
        workflow.add_node("aggregate", self._aggregate_answers)
        
        # Set entry point to first agent
        workflow.set_entry_point("agent_0")
        
        # Connect agents sequentially (you can also run them in parallel)
        for i in range(self.agents_num - 1):
            workflow.add_edge(f"agent_{i}", f"agent_{i+1}")
        
        # Last agent goes to aggregator
        workflow.add_edge(f"agent_{self.agents_num - 1}", "aggregate")
        
        # Aggregator goes to end
        workflow.add_edge("aggregate", END)
        
        return workflow
    
    def _aggregate_answers(self, state: AgentState) -> AgentState:
        """Aggregate answers from all agents using majority voting."""
        print("Aggregating answers from all agents", flush=True)
        
        agent_answers = state["agent_answers"]
        final_answer = self.final_answer_fn(agent_answers, state.get("question_data", {}))
        
        return {
            "final_answer": final_answer
        }
    
    def forward(self, question_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a question through the multi-agent system."""
        # Initialize state
        initial_state = {
            "question": question_data["state"],
            "question_type": self.question_type,
            "agent_responses": [],
            "agent_answers": [],
            "final_answer": "",
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "ground_truth": question_data.get("ground_truth", ""),
            "question_data": question_data
        }
        
        # Run the graph
        final_state = self.app.invoke(initial_state)
        
        # Format result to match original interface
        result_dict = {
            "final_answer": final_state["final_answer"],
            "completions": [final_state["agent_responses"]],  # Format to match original
            "answers": [final_state["agent_answers"]],
            "total_prompt_tokens": final_state["total_prompt_tokens"],
            "total_completion_tokens": final_state["total_completion_tokens"],
        }
        
        return result_dict
