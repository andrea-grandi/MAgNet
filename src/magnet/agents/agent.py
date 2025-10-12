from typing import Any, List, Dict, Optional, Callable
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage

from .state import AgentState



class Agent:
    """
    LangGraph-based Agent implementation.
    
    This agent is designed to work with LangGraph's state management system,
    replacing the original imperative-style agent from AgentForest.
    """
    
    def __init__(
        self, 
        role: str, 
        mtype: str, 
        ans_parser: Callable,
        qtype: str, 
        nums: int = 1, 
        temperature: float = 1.0, 
        top_p: float = 1.0
    ) -> None:
        """
        Initialize an Agent.
        
        Args:
            role: The role of the agent (e.g., "solver", "verifier")
            mtype: Model type (e.g., "gpt-35-turbo", "gpt-4", "llama2")
            ans_parser: Function to parse answers from agent responses
            qtype: Question type (e.g., "math", "mmlu", "code_completion", "chess", "gsm")
            nums: Number of responses to generate (for sampling)
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
        """

        self.role = role
        self.mtype = mtype
        self.qtype = qtype
        self.ans_parser = ans_parser
        self.reply = None
        self.answer = ""
        self.question = None
        self.llm_ip = None
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.nums = nums
        self.temperature = temperature
        self.top_p = top_p
        
        # Model configuration
        self.model, self.llm_ip = self._configure_model(mtype)
        
        # Build the LangGraph workflow
        self.graph = self._build_graph()
        
    def _configure_model(self, mtype: str) -> tuple[str, Optional[str]]:
        """
        Configure the model based on the model type.
        
        Args:
            mtype: Model type string
            
        Returns:
            Tuple of (model_name, llm_ip)
        """

        llm_ip = None
        
        if mtype == "gpt-35-turbo":
            model = "gpt-35-turbo"
        elif mtype == "gpt-4":
            model = "gpt-4"
        elif mtype == "gpt-4-1106-Preview":
            model = "gpt-4-1106-Preview"
        elif mtype == "gpt-35-turbo-1106":
            model = "gpt-35-turbo-1106"
        else:
            # Open-source LLM
            model = mtype
            llm_ip = get_llama_ip()
            
        return model, llm_ip
    
    def _build_graph(self) -> CompiledStateGraph:
        """
        Build the LangGraph workflow for the agent.
        
        Returns:
            Compiled state graph
        """

        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("preprocess", self._preprocess_node)
        workflow.add_node("generate", self._generate_node)
        workflow.add_node("postprocess", self._postprocess_node)
        
        # Define edges
        workflow.set_entry_point("preprocess")
        workflow.add_edge("preprocess", "generate")
        workflow.add_edge("generate", "postprocess")
        workflow.add_edge("postprocess", END)
        
        return workflow.compile()
    
    def _get_system_prompt(self) -> str:
        """
        Get the system prompt based on question type.
        
        Returns:
            System prompt string
        """
        if self.qtype == "code_completion":
            return ""  # Can add CODE_COMPLETION_SYSTEM_PROMPT if needed
        elif self.qtype == "mmlu":
            return ""
        elif self.qtype == "math":
            return ""  # Can add MATH_TASK_SYSTEM_PROMPT if needed
        elif self.qtype == "chess":
            return ""
        elif self.qtype == "gsm":
            return ""
        else:
            return ""
    
    def _get_context(self, question: Optional[str]) -> List[Dict[str, str]]:
        """
        Build the conversation context for the LLM.
        
        Args:
            question: The question to answer
            
        Returns:
            List of message dictionaries
        """
        if question is None:
            return []
            
        sys_prompt = self._get_system_prompt()
        contexts = [{"role": "system", "content": sys_prompt}]
        
        # Add the question as user message
        user_message = construct_message(question, self.qtype)
        contexts.append(user_message)
        
        return contexts
    
    def _preprocess_node(self, state: AgentState) -> AgentState:
        """
        Preprocess node: Prepare the question and context.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated agent state
        """
        question = state["question"]
        
        # Store question in state
        return {
            **state,
            "question": question,
        }
    
    def _generate_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Generate node: Generate response from LLM.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated agent state with LLM response
        """
        question = state["question"]
        
        # Build context
        contexts = self._get_context(question)
        
        # Convert to LangChain messages
        messages: List[BaseMessage] = []
        for ctx in contexts:
            if ctx["role"] == "system":
                messages.append(SystemMessage(content=ctx["content"]))
            elif ctx["role"] == "user":
                messages.append(HumanMessage(content=ctx["content"]))
            elif ctx["role"] == "assistant":
                messages.append(AIMessage(content=ctx["content"]))
        
        # Initialize LLM
        if self.llm_ip:
            # For open-source models with custom endpoint
            import os
            # Set temporary API key for open-source models
            os.environ.setdefault("OPENAI_API_KEY", "none")
            llm = ChatOpenAI(
                model=self.model,
                temperature=self.temperature,
                model_kwargs={"top_p": self.top_p},
                base_url=f"http://{self.llm_ip}/v1",
            )
        else:
            # For OpenAI models
            llm = ChatOpenAI(
                model=self.model,
                temperature=self.temperature,
                model_kwargs={"top_p": self.top_p},
            )
        
        # Generate response
        response = llm.invoke(messages)
        
        # Extract token usage if available
        prompt_tokens = 0
        completion_tokens = 0
        if hasattr(response, 'response_metadata'):
            usage = response.response_metadata.get('token_usage', {})
            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)
        
        return {
            "reply": response.content,
            "prompt_tokens": state.get("prompt_tokens", 0) + prompt_tokens,
            "completion_tokens": state.get("completion_tokens", 0) + completion_tokens,
        }
    
    def _postprocess_node(self, state: AgentState) -> AgentState:
        """
        Postprocess node: Parse the answer from the response.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated agent state with parsed answer
        """
        reply = state["reply"]
        question = state["question"]
        
        # Parse the answer using the provided parser
        answer, _ = self.ans_parser(reply, question)
        
        return {
            **state,
            "answer": answer if answer is not None else "",
        }
    
    def invoke(self, question: str) -> Dict[str, Any]:
        """
        Run the agent on a question (synchronous).
        
        Args:
            question: The question to answer
            
        Returns:
            Final agent state
        """
        initial_state: AgentState = {
            "role": self.role,
            "mtype": [self.mtype],
            "qtype": [self.qtype],
            "ans_parser": self.ans_parser.__name__ if hasattr(self.ans_parser, '__name__') else str(self.ans_parser),
            "reply": None,
            "answer": "",
            "question": question,
            "llm_ip": self.llm_ip,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "nums": self.nums,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "model": self.model,
        }
        
        result = self.graph.invoke(initial_state)
        return result  # type: ignore
    
    async def ainvoke(self, question: str) -> Dict[str, Any]:
        """
        Run the agent on a question (asynchronous).
        
        Args:
            question: The question to answer
            
        Returns:
            Final agent state
        """
        initial_state: AgentState = {
            "role": self.role,
            "mtype": [self.mtype],
            "qtype": [self.qtype],
            "ans_parser": self.ans_parser.__name__ if hasattr(self.ans_parser, '__name__') else str(self.ans_parser),
            "reply": None,
            "answer": "",
            "question": question,
            "llm_ip": self.llm_ip,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "nums": self.nums,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "model": self.model,
        }
        
        result = await self.graph.ainvoke(initial_state)
        return result  # type: ignore
    
    def get_reply(self, state: Dict[str, Any]) -> Optional[str]:
        """
        Get the reply from the agent state.
        
        Args:
            state: Agent state
            
        Returns:
            Reply string or None
        """
        return state.get("reply")
    
    def get_answer(self, state: Dict[str, Any]) -> str:
        """
        Get the parsed answer from the agent state.
        
        Args:
            state: Agent state
            
        Returns:
            Answer string
        """
        return state.get("answer", "")
    
    def preprocess(self, question: str) -> List[Dict[str, str]]:
        """
        Preprocess the question to build context (compatibility method).
        
        Args:
            question: The question to answer
            
        Returns:
            List of message dictionaries (context)
        """
        return self._get_context(question)
    
    def postprocess(self, completion: str, question: str) -> tuple[str, Any]:
        """
        Postprocess the completion to extract the answer (compatibility method).
        
        Args:
            completion: The LLM completion
            question: The original question
            
        Returns:
            Tuple of (answer, metadata)
        """
        answer, metadata = self.ans_parser(completion, question)
        return answer if answer is not None else "", metadata


class AgentFactory:
    """
    Factory class for creating agents with different configurations.
    """
    
    @staticmethod
    def create_agent(
        role: str,
        mtype: str,
        ans_parser: Callable,
        qtype: str,
        nums: int = 1,
        temperature: float = 1.0,
        top_p: float = 1.0
    ) -> Agent:
        """
        Create an agent with the specified configuration.
        
        Args:
            role: The role of the agent
            mtype: Model type
            ans_parser: Answer parsing function
            qtype: Question type
            nums: Number of responses
            temperature: Sampling temperature
            top_p: Top-p sampling
            
        Returns:
            Configured Agent instance
        """
        return Agent(
            role=role,
            mtype=mtype,
            ans_parser=ans_parser,
            qtype=qtype,
            nums=nums,
            temperature=temperature,
            top_p=top_p
        )
    
    @staticmethod
    def create_batch_agents(
        num_agents: int,
        role: str,
        mtype: str,
        ans_parser: Callable,
        qtype: str,
        nums: int = 1,
        temperature: float = 1.0,
        top_p: float = 1.0
    ) -> List[Agent]:
        """
        Create multiple identical agents for ensemble methods (AgentForest pattern).
        
        Args:
            num_agents: Number of agents to create
            role: The role of the agents
            mtype: Model type
            ans_parser: Answer parsing function
            qtype: Question type
            nums: Number of responses
            temperature: Sampling temperature
            top_p: Top-p sampling
            
        Returns:
            List of Agent instances
        """
        return [
            AgentFactory.create_agent(
                role=role,
                mtype=mtype,
                ans_parser=ans_parser,
                qtype=qtype,
                nums=nums,
                temperature=temperature,
                top_p=top_p
            )
            for _ in range(num_agents)
        ]


