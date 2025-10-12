from typing import TypedDict, Annotated, Literal, Any, Callable
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from .state import AgentState
from magnet.utils.utils import get_llama_ip


class Agent:
    def __init__(self, role, mtype, ans_parser, qtype, nums=1, temperature=1, top_p=1):
        self.role = role
        self.mtype = mtype
        self.qtype = qtype
        self.ans_parser = ans_parser
        self.nums = nums
        self.temperature = temperature
        self.top_p = top_p
        self.llm_ip = None
        
        # Inizializza il modello
        self._init_model(mtype)
        
        # Crea il grafo
        self.graph = self._build_graph()
    
    def _init_model(self, mtype):
        """Inizializza il modello LLM appropriato"""
        if mtype in ["gpt-35-turbo", "gpt-4", "gpt-4-1106-Preview", "gpt-35-turbo-1106"]:
            self.model = ChatOpenAI(
                model=mtype,
                temperature=self.temperature,
                top_p=self.top_p,
                n=self.nums
            )
        else:
            self.llm_ip = get_llama_ip()
            self.model = ChatOpenAI(
                model=mtype,
                temperature=self.temperature,
                top_p=self.top_p,
                n=self.nums,
                base_url=self.llm_ip
            )
    
    def _get_system_prompt(self, qtype):
        """Ottiene il system prompt in base al tipo di domanda"""
        prompts = {
            "code_completion": "",
            "mmlu": "",
            "math": "",
            "chess": "",
            "gsm": "",
            "istask": "",
            "sstask": ""
        }
        
        if qtype not in prompts:
            raise NotImplementedError(f"Question type {qtype} not implemented")
        
        return prompts[qtype]
    
    def preprocess_node(self, state: AgentState) -> AgentState:
        """Nodo di preprocessing: prepara i contesti"""
        sys_prompt = self._get_system_prompt(self.qtype)
        contexts = [{"role": "system", "content": sys_prompt}]
        
        return {
            **state,
            "contexts": contexts
        }
    
    def llm_node(self, state: AgentState) -> AgentState:
        """Nodo LLM: esegue la chiamata al modello"""
        # Prepara i messaggi
        messages = []
        for ctx in state["contexts"]:
            if ctx["role"] == "system":
                messages.append(SystemMessage(content=ctx["content"]))
            elif ctx["role"] == "user":
                messages.append(HumanMessage(content=ctx["content"]))
        
        # Aggiungi la domanda corrente
        messages.append(HumanMessage(content=state["question"])) # type: ignore
        
        # Chiamata al modello
        response = self.model.invoke(messages)
        
        # Estrai token usage se disponibile
        prompt_tokens = 0
        completion_tokens = 0
        if hasattr(response, "response_metadata"):
            usage = response.response_metadata.get("token_usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
        
        return {
            **state,
            "reply": response.content, # type: ignore
            "prompt_tokens": state.get("prompt_tokens", 0) + prompt_tokens,
            "completion_tokens": state.get("completion_tokens", 0) + completion_tokens
        }
    
    def postprocess_node(self, state: AgentState) -> AgentState:
        """Nodo di postprocessing: analizza la risposta"""
        answer, _ = self.ans_parser(state["reply"], state["question"])
        
        return {
            **state,
            "answer": answer
        }
    
    def _build_graph(self) -> CompiledStateGraph:
        """Costruisce il grafo LangGraph"""
        workflow = StateGraph(AgentState)
        
        # Aggiungi i nodi
        workflow.add_node("preprocess", self.preprocess_node)
        workflow.add_node("llm", self.llm_node)
        workflow.add_node("postprocess", self.postprocess_node)
        
        # Definisci gli edge
        workflow.set_entry_point("preprocess")
        workflow.add_edge("preprocess", "llm")
        workflow.add_edge("llm", "postprocess")
        workflow.add_edge("postprocess", END)
        
        return workflow.compile()
    
    def run(self, question: str) -> AgentState:
        """Esegue l'agente con una domanda"""
        initial_state = {
            "question": question,
            "contexts": [],
            "reply": None,
            "answer": None,
            "prompt_tokens": 0,
            "completion_tokens": 0
        }
        
        result = self.graph.invoke(initial_state)
        return result
    
    def get_reply(self, state: AgentState) -> str:
        """Ottiene la risposta raw"""
        return state.get("reply", "") # type: ignore
    
    def get_answer(self, state: AgentState) -> str:
        """Ottiene la risposta parsata"""
        return state.get("answer", "") # type: ignore