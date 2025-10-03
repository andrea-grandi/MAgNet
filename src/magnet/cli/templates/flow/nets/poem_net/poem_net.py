from magnet import Agent, Net, Process, Task
from magnet.project import NetBase, agent, net, task
from magnet.agents.agent_builder.base_agent import BaseAgent
from typing import List

# If you want to run a snippet of code before or after the net starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.magnet.com/concepts/crews#example-net-class-with-decorators


@NetBase
class PoemNet:
    """Poem Net"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.magnet.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.magnet.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your net, you can learn more about it here:
    # https://docs.magnet.com/concepts/agents#agent-tools
    @agent
    def poem_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["poem_writer"],  # type: ignore[index]
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.magnet.com/concepts/tasks#overview-of-a-task
    @task
    def write_poem(self) -> Task:
        return Task(
            config=self.tasks_config["write_poem"],  # type: ignore[index]
        )

    @net
    def net(self) -> Net:
        """Creates the Research Net"""
        # To learn how to add knowledge sources to your net, check out the documentation:
        # https://docs.magnet.com/concepts/knowledge#what-is-knowledge

        return Net(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
