from __future__ import annotations

import json
import os
import random

from typing import List, Dict, Any, Set, Optional
from dataclasses import dataclass
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage


@dataclass
class CustomAgentConfig:
    name_prefix: str
    num: int
    min_before_final: int = 3
    max_turns: Optional[int] = None
    max_chars_per_contribution: Optional[int] = None
    log_dir: Optional[str] = None
    randomize_order: bool = True


class CooperativeAgentOrchestrator:
    """A lightweight custom orchestrator that enforces multi-agent handoffs.

    It does NOT rely on create_react_agent. Instead it manually cycles agents,
    prompting each one to add a short contribution until the threshold is reached.
    """

    def __init__(self, llm, config: CustomAgentConfig, base_prompt: str):
        self.llm = llm
        self.config = config
        self.base_prompt = base_prompt
        if self.config.log_dir:
            os.makedirs(self.config.log_dir, exist_ok=True)
        self._log_file = (
            os.path.join(self.config.log_dir, f"swarm_run_{datetime.utcnow().isoformat().replace(':','-')}.jsonl")
            if self.config.log_dir else None
        )

    def _agent_name(self, idx: int) -> str:
        return f"{self.config.name_prefix}_{idx}"

    def _count_agents(self, messages: List[Any]) -> Set[str]:
        agents: Set[str] = set()
        for m in messages:
            if isinstance(m, AIMessage) and m.name:
                agents.add(m.name)
        return agents

    def _build_agent_prompt(self, idx: int, messages: List[Any]) -> str:
        prior_agents = self._count_agents(messages)
        # Compose a concise conversation transcript summary
        history_parts = []
        for m in messages[-6:]:  # last few only
            role = 'Human' if isinstance(m, HumanMessage) else (m.name or 'AI')
            snippet = str(m.content)
            if len(snippet) > 400:
                snippet = snippet[:400] + '...'
            history_parts.append(f"[{role}] {snippet}")
        history = '\n'.join(history_parts) or '(no prior messages)'

        need_final = len(prior_agents) >= self.config.min_before_final - 1  # -1 because current will be added

        # Allow dynamic base prompt with placeholders. Available placeholders:
        # {agent_name}, {prior_agents}, {need_final}, {num_agents}, {history}
        agent_name = self._agent_name(idx)
        base = self.base_prompt or "You are agent {agent_name} in a cooperative swarm."
        try:
            base_filled = base.format(
                agent_name=agent_name,
                prior_agents=", ".join(sorted(prior_agents)) or "none",
                need_final=str(need_final),
                num_agents=self.config.num,
                history=history,
            )
        except KeyError:
            # Fallback if user didn't provide all placeholders
            base_filled = base

        instructions = [
            base_filled,
            "Conversation so far:",
            history,
            f"Agents who already contributed: {', '.join(sorted(prior_agents)) or 'none'}",
        ]
        if not need_final:
            instructions.append(
                "Provide a SHORT incremental reasoning step (2-4 sentences max), DO NOT give the final answer yet."
            )
        else:
            instructions.append(
                "Now synthesize all reasoning and provide the FINAL answer in the form 'Final Answer: <number>'."
            )
        return '\n\n'.join(instructions)

    def _truncate(self, text: str) -> str:
        if self.config.max_chars_per_contribution and len(text) > self.config.max_chars_per_contribution:
            return text[: self.config.max_chars_per_contribution] + "... [truncated]"
        return text

    def _log(self, payload: Dict[str, Any]):
        if not self._log_file:
            return
        with open(self._log_file, 'a') as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def run(self, user_question: str) -> Dict[str, Any]:
        messages: List[Any] = [HumanMessage(content=user_question)]
        turns_limit = self.config.max_turns or self.config.num

        # Determine processing order
        candidate_indices = list(range(self.config.num))
        if self.config.randomize_order:
            random.shuffle(candidate_indices)

        turns_executed = 0
        for idx in candidate_indices:
            if turns_executed >= turns_limit:
                break
            prior_agents = self._count_agents(messages)
            if len(prior_agents) >= self.config.min_before_final:
                break
            prompt = self._build_agent_prompt(idx, messages)
            response = self.llm.invoke(prompt)
            truncated = self._truncate(response.content)
            ai_msg = AIMessage(content=truncated, name=self._agent_name(idx))
            messages.append(ai_msg)
            self._log({
                "type": "agent_turn",
                "agent": ai_msg.name,
                "turn_index": turns_executed,
                "original_index": idx,
                "truncated": truncated != response.content,
                "content": ai_msg.content,
                "num_prior_agents": len(prior_agents),
                "need_final": len(prior_agents) >= self.config.min_before_final - 1,
                "order_randomized": self.config.randomize_order,
                "timestamp": datetime.utcnow().isoformat()
            })
            turns_executed += 1
            if "Final Answer:" in ai_msg.content:
                break
        else:
            self._log({
                "type": "loop_complete_without_final",
                "turns_executed": turns_executed,
                "timestamp": datetime.utcnow().isoformat()
            })

        # If no final answer, ask one more synthesis pass
        if not any(isinstance(m, AIMessage) and "Final Answer:" in str(m.content) for m in messages):
            synthesis_prompt = (
                "You are a synthesis agent. Read the following contributions and provide the final answer as 'Final Answer: <number>'.\n\n" +
                '\n'.join(
                    f"{m.name}: {m.content}" for m in messages if isinstance(m, AIMessage)
                ) + f"\n\nQuestion: {user_question}"
            )
            synth_resp = self.llm.invoke(synthesis_prompt)
            truncated_syn = self._truncate(synth_resp.content)
            messages.append(AIMessage(content=truncated_syn, name="synthesis_agent"))
            self._log({
                "type": "synthesis",
                "agent": "synthesis_agent",
                "content": truncated_syn,
                "timestamp": datetime.utcnow().isoformat()
            })

        return {"messages": messages}
