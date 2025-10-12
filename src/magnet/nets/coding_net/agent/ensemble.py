"""
Ensemble execution engine.
Manages parallel execution of multiple agents and aggregates results.
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from collections import Counter
import numpy as np
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from ..config.loader import EnsembleConfig


class AgentResponse:
    """Represents a single agent's response."""
    
    def __init__(self, agent_id: int, content: str, temperature: float, 
                 execution_time: float, confidence: Optional[float] = None):
        self.agent_id = agent_id
        self.content = content
        self.temperature = temperature
        self.execution_time = execution_time
        self.confidence = confidence
    
    def __repr__(self):
        return f"AgentResponse(id={self.agent_id}, temp={self.temperature:.2f}, time={self.execution_time:.2f}s)"


class EnsembleExecutor:
    """Execute ensemble of agents and aggregate results."""
    
    def __init__(self, config: EnsembleConfig):
        """
        Initialize ensemble executor.
        
        Args:
            config: EnsembleConfig instance
        """
        self.config = config
        self.responses: List[AgentResponse] = []
    
    def _generate_temperatures(self) -> List[float]:
        """Generate temperature values for agents."""
        if not self.config.vary_temperature:
            return [self.config.get('ensemble.base_temperature', 0.7)] * self.config.num_agents
        
        min_temp, max_temp = self.config.temperature_range
        distribution = self.config.get('diversification.temperature_distribution', 'uniform')
        
        if distribution == 'uniform':
            temperatures = np.linspace(min_temp, max_temp, self.config.num_agents)
        elif distribution == 'normal':
            mean_temp = (min_temp + max_temp) / 2
            std_temp = (max_temp - min_temp) / 6
            temperatures = np.random.normal(mean_temp, std_temp, self.config.num_agents)
            temperatures = np.clip(temperatures, min_temp, max_temp)
        else:  # random
            temperatures = np.random.uniform(min_temp, max_temp, self.config.num_agents)
        
        return temperatures.tolist()
    
    async def _execute_single_agent(self, agent_id: int, question: str, 
                                     temperature: float, system_prompt: str) -> Optional[AgentResponse]:
        """
        Execute a single agent.
        
        Args:
            agent_id: Unique agent identifier
            question: Question to answer
            temperature: Temperature for this agent
            system_prompt: System prompt for the agent
        
        Returns:
            AgentResponse or None if failed
        """
        try:
            start_time = time.time()
            
            # Create LLM with specific temperature
            llm = ChatOpenAI(
                model=self.config.model,
                temperature=temperature,
                timeout=self.config.timeout_seconds
            )
            
            # Create messages
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=question)
            ]
            
            # Invoke LLM
            response = await llm.ainvoke(messages)
            
            execution_time = time.time() - start_time
            
            # Extract content as string
            content = response.content if isinstance(response.content, str) else str(response.content)
            
            return AgentResponse(
                agent_id=agent_id,
                content=content,
                temperature=temperature,
                execution_time=execution_time
            )
            
        except Exception as e:
            print(f"Agent {agent_id} failed: {str(e)}")
            return None
    
    async def _execute_agents_parallel(self, question: str, system_prompt: str) -> List[AgentResponse]:
        """
        Execute multiple agents in parallel with concurrency control.
        
        Args:
            question: Question to answer
            system_prompt: System prompt for agents
        
        Returns:
            List of successful AgentResponse objects
        """
        temperatures = self._generate_temperatures()
        responses = []
        
        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(self.config.max_concurrent)
        
        async def execute_with_semaphore(agent_id: int, temp: float):
            async with semaphore:
                return await self._execute_single_agent(agent_id, question, temp, system_prompt)
        
        # Create all tasks
        tasks = [
            execute_with_semaphore(i, temp) 
            for i, temp in enumerate(temperatures)
        ]
        
        # Execute with progress tracking
        print(f"Executing {self.config.num_agents} agents (max {self.config.max_concurrent} concurrent)...")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter successful responses
        for result in results:
            if isinstance(result, AgentResponse):
                responses.append(result)
                
                # Early stopping check
                if self.config.early_stopping and len(responses) >= self.config.get('performance.early_stop_min_responses', 30):
                    consensus_pct = self._calculate_consensus(responses)
                    if consensus_pct >= self.config.early_stop_threshold:
                        print(f"Early stopping: {consensus_pct*100:.1f}% consensus reached with {len(responses)} responses")
                        break
        
        return responses
    
    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts.
        Simple implementation using word overlap. 
        Can be enhanced with embeddings for better accuracy.
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score between 0 and 1
        """
        # Normalize texts
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def _cluster_responses(self, responses: List[AgentResponse]) -> Dict[str, List[AgentResponse]]:
        """
        Group similar responses together.
        
        Args:
            responses: List of agent responses
        
        Returns:
            Dictionary mapping representative response to list of similar responses
        """
        clusters = {}
        threshold = self.config.similarity_threshold
        
        for response in responses:
            # Find if this response belongs to an existing cluster
            matched = False
            for representative, cluster in clusters.items():
                similarity = self._calculate_semantic_similarity(response.content, representative)
                if similarity >= threshold:
                    cluster.append(response)
                    matched = True
                    break
            
            # Create new cluster if no match
            if not matched:
                clusters[response.content] = [response]
        
        return clusters
    
    def _calculate_consensus(self, responses: List[AgentResponse]) -> float:
        """
        Calculate consensus percentage among responses.
        
        Args:
            responses: List of agent responses
        
        Returns:
            Consensus percentage (0-1)
        """
        if not responses:
            return 0.0
        
        clusters = self._cluster_responses(responses)
        largest_cluster_size = max(len(cluster) for cluster in clusters.values())
        
        return largest_cluster_size / len(responses)
    
    def _majority_vote(self, responses: List[AgentResponse]) -> Dict[str, Any]:
        """
        Perform majority voting on responses.
        
        Args:
            responses: List of agent responses
        
        Returns:
            Dictionary with winning response and metadata
        """
        # Cluster similar responses
        clusters = self._cluster_responses(responses)
        
        # Sort clusters by size (descending)
        sorted_clusters = sorted(
            clusters.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        # Get the winning cluster
        winning_response, winning_cluster = sorted_clusters[0]
        consensus_pct = len(winning_cluster) / len(responses)
        
        # Check if consensus meets minimum threshold
        min_consensus = self.config.min_consensus / 100.0
        
        result = {
            'final_answer': winning_response,
            'consensus_percentage': consensus_pct * 100,
            'num_supporting_agents': len(winning_cluster),
            'total_agents': len(responses),
            'meets_consensus': consensus_pct >= min_consensus,
            'clusters': [
                {
                    'response': resp,
                    'count': len(cluster),
                    'percentage': (len(cluster) / len(responses)) * 100
                }
                for resp, cluster in sorted_clusters[:5]  # Top 5 clusters
            ]
        }
        
        return result
    
    async def execute(self, question: str, system_prompt: str) -> Dict[str, Any]:
        """
        Execute ensemble and aggregate results.
        
        Args:
            question: Question to answer
            system_prompt: System prompt for agents
        
        Returns:
            Dictionary with final answer and metadata
        """
        start_time = time.time()
        
        # Execute agents in parallel
        if self.config.parallel_execution:
            responses = await self._execute_agents_parallel(question, system_prompt)
        else:
            # Sequential execution (not recommended for large ensembles)
            temperatures = self._generate_temperatures()
            responses = []
            for i, temp in enumerate(temperatures):
                result = await self._execute_single_agent(i, question, temp, system_prompt)
                if result:
                    responses.append(result)
        
        self.responses = responses
        
        # Check minimum successful responses
        if len(responses) < self.config.min_successful_responses:
            return {
                'error': f'Insufficient responses: {len(responses)}/{self.config.min_successful_responses} required',
                'num_successful_responses': len(responses),
                'execution_time_seconds': time.time() - start_time
            }
        
        # Aggregate based on method
        if self.config.aggregation_method == 'majority_vote':
            result = self._majority_vote(responses)
        else:
            # Fallback
            result = {
                'final_answer': responses[0].content if responses else "No response",
                'method': 'fallback'
            }
        
        # Add metadata
        execution_time = time.time() - start_time
        
        if self.config.include_metadata:
            metadata: Dict[str, Any] = {
                'num_agents_executed': self.config.num_agents,
                'num_successful_responses': len(responses),
                'execution_time_seconds': execution_time,
                'avg_response_time': float(np.mean([r.execution_time for r in responses])),
                'temperature_range': list(self.config.temperature_range),
                'aggregation_method': self.config.aggregation_method,
                'individual_responses': [
                    {
                        'agent_id': r.agent_id,
                        'content': r.content,
                        'temperature': r.temperature,
                        'execution_time': r.execution_time
                    }
                    for r in responses
                ] if self.config.get('output.log_individual_responses', False) else None
            }
            result['metadata'] = metadata # type: ignore
        
        return result


async def run_ensemble(question: str, config: Optional[EnsembleConfig] = None, 
                       system_prompt: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to run ensemble.
    
    Args:
        question: Question to answer
        config: EnsembleConfig (optional, uses default if None)
        system_prompt: System prompt (optional, uses default if None)
    
    Returns:
        Result dictionary
    """
    from ..config.loader import load_config
    from .prompts import CODING_AGENT_PROMPT
    
    if config is None:
        config = load_config()
    
    if system_prompt is None:
        system_prompt = CODING_AGENT_PROMPT
    
    executor = EnsembleExecutor(config)
    result = await executor.execute(question, system_prompt)
    
    return result
