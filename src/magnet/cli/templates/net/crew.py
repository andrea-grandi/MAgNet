from magnet import Agent, Net, Process, Task
from magnet.project import CrewBase, agent, net, task
from magnet.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the net starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.magnet.com/concepts/crews#example-net-class-with-decorators

@CrewBase
class {{crew_name}}():
    """{{crew_name}} net"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.magnet.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.magnet.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.magnet.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.magnet.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='report.md'
        )

    @net
    def net(self) -> Net:
        """Creates the {{crew_name}} net"""
        # To learn how to add knowledge sources to your net, check out the documentation:
        # https://docs.magnet.com/concepts/knowledge#what-is-knowledge

        return Net(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.magnet.com/how-to/Hierarchical/
        )
