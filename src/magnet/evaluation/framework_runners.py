import time
import psutil
import os
import traceback

from typing import Dict, List, Any, Optional

# Add project paths
#project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(project_root)
#sys.path.append(os.path.join(project_root, "agents"))
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from magnet.evaluation.task_definitions import TaskDefinition


class BaseFrameworkRunner:
    """Base class for framework runners"""
    
    def __init__(self):
        self.memory_usage = []
        self.execution_times = []
        self.token_usage = {}
    
    def _record_memory_usage(self):
        """Record current memory usage"""
        process = psutil.Process(os.getpid())
        memory_mb = process.memory_info().rss / 1024 / 1024
        self.memory_usage.append({
            'memory_mb': memory_mb,
            'timestamp': time.time()
        })
    
    def _record_token_usage(self, framework: str, tokens: int):
        """Record token usage"""
        if framework not in self.token_usage:
            self.token_usage[framework] = 0
        self.token_usage[framework] += tokens
    
    def _create_execution_result(self, 
                               achieved_goals: List[str],
                               satisfied_constraints: List[str],
                               schedule: List[Dict[str, Any]],
                               disruptions_handled: Optional[List[Dict[str, Any]]] = None,
                               replanning_attempts: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Create standardized execution result"""
        return {
            'achieved_goals': achieved_goals,
            'satisfied_constraints': satisfied_constraints,
            'schedule': schedule,
            'disruptions_handled': disruptions_handled or [],
            'replanning_attempts': replanning_attempts or [],
            'resource_usage': {
                'memory_usage': self.memory_usage,
                'execution_times': self.execution_times,
                'token_usage': self.token_usage
            }
        }


class LangGraphRunner(BaseFrameworkRunner):
    """Runner for LangGraph framework"""
    
    def __init__(self):
        super().__init__()
        try:
            # Import the router function from langgraph
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'frameworks', 'langgraph'))
            from magnet.frameworks.langgraph.router import run_agent
            self.run_agent = run_agent
        except ImportError as e:
            print(f"Warning: LangGraph not available: {e}")
            self.run_agent = None
    
    def __call__(self, task_definition: TaskDefinition) -> Dict[str, Any]:
        """Execute task using LangGraph"""
        if not self.run_agent:
            raise RuntimeError("LangGraph framework not available")
        
        start_time = time.time()
        self._record_memory_usage()
        
        try:
            # Create task description for LangGraph
            task_description = f"""
            Task: {task_definition.description}
            Goals: {[goal.description for goal in task_definition.goals]}
            Constraints: {[c.description for c in task_definition.constraints]}
            Resources: {task_definition.resources}
            """
            
            # Execute the agent
            result = self.run_agent(task_description)
            
            execution_time = time.time() - start_time
            self.execution_times.append(execution_time)
            self._record_memory_usage()
            
            # Extract results from LangGraph output
            achieved_goals = self._extract_achieved_goals(result)
            satisfied_constraints = self._extract_satisfied_constraints(result)
            schedule = self._extract_schedule(result)
            
            return self._create_execution_result(
                achieved_goals=achieved_goals,
                satisfied_constraints=satisfied_constraints,
                schedule=schedule
            )
            
        except Exception as e:
            print(f"LangGraph execution error: {str(e)}")
            traceback.print_exc()
            return self._create_execution_result([], [], [])
    
    def _extract_achieved_goals(self, result: Dict[str, Any]) -> List[str]:
        """Extract achieved goals from LangGraph result"""
        achieved_goals = []
        if 'goals_achieved' in result:
            achieved_goals = result['goals_achieved']
        elif 'goals' in result:
            achieved_goals = result['goals']
        elif 'output' in result and isinstance(result['output'], dict) and 'goals' in result['output']:
            achieved_goals = result['output']['goals']
        return achieved_goals
    
    def _extract_satisfied_constraints(self, result: Dict[str, Any]) -> List[str]:
        """Extract satisfied constraints from LangGraph result"""
        satisfied_constraints = []
        if 'constraints_satisfied' in result:
            satisfied_constraints = result['constraints_satisfied']
        elif 'constraints' in result:
            satisfied_constraints = result['constraints']
        elif 'output' in result and isinstance(result['output'], dict) and 'constraints' in result['output']:
            satisfied_constraints = result['output']['constraints']
        return satisfied_constraints
    
    def _extract_schedule(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract schedule from LangGraph result"""
        schedule = []
        if 'schedule' in result:
            schedule = result['schedule']
        elif 'output' in result and isinstance(result['output'], dict) and 'schedule' in result['output']:
            schedule = result['output']['schedule']
        return schedule





def get_framework_runners() -> Dict[str, BaseFrameworkRunner]:
    """Get all available framework runners"""
    runners = {}
    
    # Try to initialize each framework runner
    try:
        runners['langgraph'] = LangGraphRunner()
    except Exception as e:
        print(f"LangGraph runner not available: {e}")
    
    return runners


def create_mock_runner(framework_name: str) -> BaseFrameworkRunner:
    """Create a mock runner for testing when frameworks are not available"""
    
    class MockRunner(BaseFrameworkRunner):
        def __init__(self, name: str):
            super().__init__()
            self.name = name
        
        def __call__(self, task_definition: TaskDefinition) -> Dict[str, Any]:
            """Mock execution that returns basic results"""
            start_time = time.time()
            self._record_memory_usage()
            
            # Simulate some processing time
            time.sleep(1)
            
            execution_time = time.time() - start_time
            self.execution_times.append(execution_time)
            self._record_memory_usage()
            
            # Return mock results
            achieved_goals = [goal.goal_id for goal in task_definition.goals[:2]]  # Mock: achieve first 2 goals
            satisfied_constraints = [c.constraint_id for c in task_definition.constraints[:1]]  # Mock: satisfy first constraint
            
            schedule = [
                {
                    'task_id': f'task_{i}',
                    'start_time': i * 10,
                    'end_time': (i + 1) * 10,
                    'agent': f'agent_{i}'
                }
                for i in range(3)  # Mock: 3 tasks
            ]
            
            return self._create_execution_result(
                achieved_goals=achieved_goals,
                satisfied_constraints=satisfied_constraints,
                schedule=schedule
            )
    
    return MockRunner(framework_name) 