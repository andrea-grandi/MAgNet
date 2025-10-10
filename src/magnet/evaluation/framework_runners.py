import time
import psutil
import os
import traceback
import json

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
    
    def _create_execution_result(
        self, 
        achieved_goals: List[str],
        satisfied_constraints: List[str],
        schedule: List[Dict[str, Any]],
        disruptions_handled: Optional[List[Dict[str, Any]]] = None,
        replanning_attempts: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
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
            #sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'frameworks', 'langgraph'))
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
    

class CrewAIRunner(BaseFrameworkRunner):
    """Runner for CrewAI framework"""
    
    def __init__(self):
        super().__init__()
        try:
            # Import the router function from crewai
            #sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agent_frameworks', 'crewai_multi_agent'))
            from magnet.frameworks.crewai_multi_agent.router import run_crewai
            self.run_crewai = run_crewai
        except ImportError as e:
            print(f"Warning: CrewAI not available: {e}")
            self.run_crewai = None
    
    def __call__(self, task_definition: TaskDefinition) -> Dict[str, Any]:
        """Execute task using CrewAI"""
        if not self.run_crewai:
            raise RuntimeError("CrewAI framework not available")
        
        start_time = time.time()
        self._record_memory_usage()
        
        try:
            # Create task description for CrewAI
            task_description = f"""
            Task: {task_definition.description}
            Goals: {[goal.description for goal in task_definition.goals]}
            Constraints: {[c.description for c in task_definition.constraints]}
            Resources: {task_definition.resources}
            """
            
            # Execute the crew
            result = self.run_crewai(task_description)
            
            execution_time = time.time() - start_time
            self.execution_times.append(execution_time)
            self._record_memory_usage()
            
            # Extract results from CrewAI output (result is a string)
            achieved_goals = self._extract_achieved_goals(result, task_definition)
            satisfied_constraints = self._extract_satisfied_constraints(result, task_definition)
            schedule = self._extract_schedule(result)
            
            return self._create_execution_result(
                achieved_goals=achieved_goals,
                satisfied_constraints=satisfied_constraints,
                schedule=schedule
            )
            
        except Exception as e:
            print(f"CrewAI execution error: {str(e)}")
            traceback.print_exc()
            return self._create_execution_result([], [], [])
    
    def _extract_achieved_goals(self, result: str, task_definition: TaskDefinition) -> List[str]:
        """Extract achieved goals from CrewAI result string"""
        achieved_goals = []
        
        # Try to parse JSON if the result is JSON formatted
        try:
            result_dict = json.loads(result)
            # Check for various possible keys
            for key in ['goals_achieved', 'goals', 'Achieved Goals', 'Goals Achieved', 
                       'achieved_goals', 'GoalsAchieved']:
                if key in result_dict:
                    goals_list = result_dict[key]
                    # Handle both list of IDs and list of descriptions
                    if isinstance(goals_list, list):
                        for goal_item in goals_list:
                            # Try to match the goal description to a goal ID
                            for goal in task_definition.goals:
                                if isinstance(goal_item, str):
                                    # Check if it's the ID or the description matches
                                    if (goal.goal_id.lower() == goal_item.lower() or 
                                        goal.description.lower() == goal_item.lower() or
                                        goal.description.lower() in goal_item.lower()):
                                        if goal.goal_id not in achieved_goals:
                                            achieved_goals.append(goal.goal_id)
                    break
        except (json.JSONDecodeError, TypeError):
            # Result is plain text, try to match goals based on keywords
            result_lower = result.lower() if isinstance(result, str) else ""
            for goal in task_definition.goals:
                # Check if goal description or ID appears in the result
                if goal.goal_id.lower() in result_lower or goal.description.lower() in result_lower:
                    achieved_goals.append(goal.goal_id)
                else:
                    # Also check for partial matches with key terms from the goal
                    # Extract key terms (words longer than 3 chars, excluding common words)
                    common_words = {'the', 'and', 'for', 'from', 'with', 'all', 'are', 'this', 'that', 'have'}
                    goal_terms = [word for word in goal.description.lower().split() 
                                 if len(word) > 3 and word not in common_words]
                    # If at least 50% of key terms appear in the result, consider it achieved
                    if goal_terms:
                        matches = sum(1 for term in goal_terms if term in result_lower)
                        if matches / len(goal_terms) >= 0.5:
                            achieved_goals.append(goal.goal_id)
        
        return achieved_goals
    
    def _extract_satisfied_constraints(self, result: str, task_definition: TaskDefinition) -> List[str]:
        """Extract satisfied constraints from CrewAI result string"""
        satisfied_constraints = []
        
        # Try to parse JSON if the result is JSON formatted
        try:
            result_dict = json.loads(result)
            # Check for various possible keys
            for key in ['constraints_satisfied', 'constraints', 'Satisfied Constraints', 
                       'Constraints Satisfied', 'satisfied_constraints', 'ConstraintsSatisfied']:
                if key in result_dict:
                    constraints_list = result_dict[key]
                    # Handle both list of IDs and list of descriptions
                    if isinstance(constraints_list, list):
                        for constraint_item in constraints_list:
                            # Try to match the constraint description to a constraint ID
                            for constraint in task_definition.constraints:
                                if isinstance(constraint_item, str):
                                    # Check if it's the ID or the description matches
                                    if (constraint.constraint_id.lower() == constraint_item.lower() or 
                                        constraint.description.lower() == constraint_item.lower() or
                                        constraint.description.lower() in constraint_item.lower()):
                                        if constraint.constraint_id not in satisfied_constraints:
                                            satisfied_constraints.append(constraint.constraint_id)
                    break
        except (json.JSONDecodeError, TypeError):
            # Result is plain text, try to match constraints based on keywords
            result_lower = result.lower() if isinstance(result, str) else ""
            for constraint in task_definition.constraints:
                # Check if constraint description or ID appears in the result
                if constraint.constraint_id.lower() in result_lower or constraint.description.lower() in result_lower:
                    satisfied_constraints.append(constraint.constraint_id)
                else:
                    # Also check for partial matches with key terms from the constraint
                    # Extract key terms (words longer than 3 chars, excluding common words)
                    common_words = {'the', 'and', 'for', 'from', 'with', 'all', 'are', 'this', 'that', 'have'}
                    constraint_terms = [word for word in constraint.description.lower().split() 
                                       if len(word) > 3 and word not in common_words]
                    # If at least 50% of key terms appear in the result, consider it satisfied
                    if constraint_terms:
                        matches = sum(1 for term in constraint_terms if term in result_lower)
                        if matches / len(constraint_terms) >= 0.5:
                            satisfied_constraints.append(constraint.constraint_id)
        
        return satisfied_constraints
    
    def _extract_schedule(self, result: str) -> List[Dict[str, Any]]:
        """Extract schedule from CrewAI result string"""
        schedule = []
        
        # Try to parse JSON if the result is JSON formatted
        try:
            result_dict = json.loads(result)
            if 'schedule' in result_dict:
                schedule = result_dict['schedule']
        except (json.JSONDecodeError, TypeError):
            # Result is plain text, cannot extract structured schedule
            # Return empty schedule for now
            pass
        
        return schedule


def get_framework_runners() -> Dict[str, BaseFrameworkRunner]:
    """Get all available framework runners"""

    runners = {}
    
    # Try to initialize each framework runner
    try:
        runners['langgraph'] = LangGraphRunner()
    except Exception as e:
        print(f"LangGraph runner not available: {e}")

    try:
        runners['crewai'] = CrewAIRunner()
    except Exception as e:
        print(f"CrewAI runner not available: {e}")
    
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