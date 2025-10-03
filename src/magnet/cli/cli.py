import os
import subprocess
from importlib.metadata import version as get_version

import click

from magnet.cli.add_net_to_flow import add_crew_to_flow
from magnet.cli.config import Settings
from magnet.cli.create_net import create_crew
from magnet.cli.create_flow import create_flow
from magnet.cli.net_chat import run_chat
from magnet.cli.settings.main import SettingsCommand
from magnet.cli.utils import build_env_with_tool_repository_credentials, read_toml
from magnet.memory.storage.kickoff_task_outputs_storage import (
    KickoffTaskOutputsSQLiteStorage,
)

from .authentication.main import AuthenticationCommand
from .deploy.main import DeployCommand
from .enterprise.main import EnterpriseConfigureCommand
from .evaluate_net import evaluate_crew
from .install_net import install_crew
from .kickoff_flow import kickoff_flow
from .organization.main import OrganizationCommand
from .plot_flow import plot_flow
from .replay_from_task import replay_task_command
from .reset_memories_command import reset_memories_command
from .run_net import run_crew
from .tools.main import ToolCommand
from .train_net import train_crew
from .update_net import update_crew


@click.group()
@click.version_option(get_version("magnet"))
def magnet():
    """Top-level command group for magnet."""


@magnet.command(
    name="uv",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.argument("uv_args", nargs=-1, type=click.UNPROCESSED)
def uv(uv_args):
    """A wrapper around uv commands that adds custom tool authentication through env vars."""
    env = os.environ.copy()
    try:
        pyproject_data = read_toml()
        sources = pyproject_data.get("tool", {}).get("uv", {}).get("sources", {})

        for source_config in sources.values():
            if isinstance(source_config, dict):
                index = source_config.get("index")
                if index:
                    index_env = build_env_with_tool_repository_credentials(index)
                    env.update(index_env)
    except (FileNotFoundError, KeyError) as e:
        raise SystemExit(
            "Error. A valid pyproject.toml file is required. Check that a valid pyproject.toml file exists in the current directory."
        ) from e
    except Exception as e:
        raise SystemExit(f"Error: {e}") from e

    try:
        subprocess.run(  # noqa: S603
            ["uv", *uv_args],  # noqa: S607
            capture_output=False,
            env=env,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        click.secho(f"uv command failed with exit code {e.returncode}", fg="red")
        raise SystemExit(e.returncode) from e


@magnet.command()
@click.argument("type", type=click.Choice(["net", "flow"]))
@click.argument("name")
@click.option("--provider", type=str, help="The provider to use for the net")
@click.option("--skip_provider", is_flag=True, help="Skip provider validation")
def create(type, name, provider, skip_provider=False):
    """Create a new net, or flow."""
    if type == "net":
        create_crew(name, provider, skip_provider)
    elif type == "flow":
        create_flow(name)
    else:
        click.secho("Error: Invalid type. Must be 'net' or 'flow'.", fg="red")


@magnet.command()
@click.option(
    "--tools", is_flag=True, help="Show the installed version of magnet tools"
)
def version(tools):
    """Show the installed version of magnet."""
    try:
        crewai_version = get_version("magnet")
    except Exception:
        crewai_version = "unknown version"
    click.echo(f"magnet version: {crewai_version}")

    if tools:
        try:
            tools_version = get_version("magnet")
            click.echo(f"magnet tools version: {tools_version}")
        except Exception:
            click.echo("magnet tools not installed")


@magnet.command()
@click.option(
    "-n",
    "--n_iterations",
    type=int,
    default=5,
    help="Number of iterations to train the net",
)
@click.option(
    "-f",
    "--filename",
    type=str,
    default="trained_agents_data.pkl",
    help="Path to a custom file for training",
)
def train(n_iterations: int, filename: str):
    """Train the net."""
    click.echo(f"Training the Net for {n_iterations} iterations")
    train_crew(n_iterations, filename)


@magnet.command()
@click.option(
    "-t",
    "--task_id",
    type=str,
    help="Replay the net from this task ID, including all subsequent tasks.",
)
def replay(task_id: str) -> None:
    """
    Replay the net execution from a specific task.

    Args:
        task_id (str): The ID of the task to replay from.
    """
    try:
        click.echo(f"Replaying the net from task {task_id}")
        replay_task_command(task_id)
    except Exception as e:
        click.echo(f"An error occurred while replaying: {e}", err=True)


@magnet.command()
def log_tasks_outputs() -> None:
    """
    Retrieve your latest net.kickoff() task outputs.
    """
    try:
        storage = KickoffTaskOutputsSQLiteStorage()
        tasks = storage.load()

        if not tasks:
            click.echo(
                "No task outputs found. Only net kickoff task outputs are logged."
            )
            return

        for index, task in enumerate(tasks, 1):
            click.echo(f"Task {index}: {task['task_id']}")
            click.echo(f"Description: {task['expected_output']}")
            click.echo("------")

    except Exception as e:
        click.echo(f"An error occurred while logging task outputs: {e}", err=True)


@magnet.command()
@click.option("-l", "--long", is_flag=True, help="Reset LONG TERM memory")
@click.option("-s", "--short", is_flag=True, help="Reset SHORT TERM memory")
@click.option("-e", "--entities", is_flag=True, help="Reset ENTITIES memory")
@click.option("-kn", "--knowledge", is_flag=True, help="Reset KNOWLEDGE storage")
@click.option(
    "-akn", "--agent-knowledge", is_flag=True, help="Reset AGENT KNOWLEDGE storage"
)
@click.option(
    "-k", "--kickoff-outputs", is_flag=True, help="Reset LATEST KICKOFF TASK OUTPUTS"
)
@click.option("-a", "--all", is_flag=True, help="Reset ALL memories")
def reset_memories(
    long: bool,
    short: bool,
    entities: bool,
    knowledge: bool,
    kickoff_outputs: bool,
    agent_knowledge: bool,
    all: bool,
) -> None:
    """
    Reset the net memories (long, short, entity, latest_crew_kickoff_ouputs, knowledge, agent_knowledge). This will delete all the data saved.
    """
    try:
        memory_types = [
            long,
            short,
            entities,
            knowledge,
            agent_knowledge,
            kickoff_outputs,
            all,
        ]
        if not any(memory_types):
            click.echo(
                "Please specify at least one memory type to reset using the appropriate flags."
            )
            return
        reset_memories_command(
            long, short, entities, knowledge, agent_knowledge, kickoff_outputs, all
        )
    except Exception as e:
        click.echo(f"An error occurred while resetting memories: {e}", err=True)


@magnet.command()
@click.option(
    "-n",
    "--n_iterations",
    type=int,
    default=3,
    help="Number of iterations to Test the net",
)
@click.option(
    "-m",
    "--model",
    type=str,
    default="gpt-4o-mini",
    help="LLM Model to run the tests on the Net. For now only accepting only OpenAI models.",
)
def test(n_iterations: int, model: str):
    """Test the net and evaluate the results."""
    click.echo(f"Testing the net for {n_iterations} iterations with model {model}")
    evaluate_crew(n_iterations, model)


@magnet.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.pass_context
def install(context):
    """Install the Net."""
    install_crew(context.args)


@magnet.command()
def run():
    """Run the Net."""
    run_crew()


@magnet.command()
def update():
    """Update the pyproject.toml of the Net project to use uv."""
    update_crew()


@magnet.command()
def login():
    """Sign Up/Login to CrewAI Enterprise."""
    Settings().clear_user_settings()
    AuthenticationCommand().login()


# DEPLOY CREWAI+ COMMANDS
@magnet.group()
def deploy():
    """Deploy the Net CLI group."""


@deploy.command(name="create")
@click.option("-y", "--yes", is_flag=True, help="Skip the confirmation prompt")
def deploy_create(yes: bool):
    """Create a Net deployment."""
    deploy_cmd = DeployCommand()
    deploy_cmd.create_crew(yes)


@deploy.command(name="list")
def deploy_list():
    """List all deployments."""
    deploy_cmd = DeployCommand()
    deploy_cmd.list_crews()


@deploy.command(name="push")
@click.option("-u", "--uuid", type=str, help="Net UUID parameter")
def deploy_push(uuid: str | None):
    """Deploy the Net."""
    deploy_cmd = DeployCommand()
    deploy_cmd.deploy(uuid=uuid)


@deploy.command(name="status")
@click.option("-u", "--uuid", type=str, help="Net UUID parameter")
def deply_status(uuid: str | None):
    """Get the status of a deployment."""
    deploy_cmd = DeployCommand()
    deploy_cmd.get_crew_status(uuid=uuid)


@deploy.command(name="logs")
@click.option("-u", "--uuid", type=str, help="Net UUID parameter")
def deploy_logs(uuid: str | None):
    """Get the logs of a deployment."""
    deploy_cmd = DeployCommand()
    deploy_cmd.get_crew_logs(uuid=uuid)


@deploy.command(name="remove")
@click.option("-u", "--uuid", type=str, help="Net UUID parameter")
def deploy_remove(uuid: str | None):
    """Remove a deployment."""
    deploy_cmd = DeployCommand()
    deploy_cmd.remove_crew(uuid=uuid)


@magnet.group()
def tool():
    """Tool Repository related commands."""


@tool.command(name="create")
@click.argument("handle")
def tool_create(handle: str):
    tool_cmd = ToolCommand()
    tool_cmd.create(handle)


@tool.command(name="install")
@click.argument("handle")
def tool_install(handle: str):
    tool_cmd = ToolCommand()
    tool_cmd.login()
    tool_cmd.install(handle)


@tool.command(name="publish")
@click.option(
    "--force",
    is_flag=True,
    show_default=True,
    default=False,
    help="Bypasses Git remote validations",
)
@click.option("--public", "is_public", flag_value=True, default=False)
@click.option("--private", "is_public", flag_value=False)
def tool_publish(is_public: bool, force: bool):
    tool_cmd = ToolCommand()
    tool_cmd.login()
    tool_cmd.publish(is_public, force)


@magnet.group()
def flow():
    """Flow related commands."""


@flow.command(name="kickoff")
def flow_run():
    """Kickoff the Flow."""
    click.echo("Running the Flow")
    kickoff_flow()


@flow.command(name="plot")
def flow_plot():
    """Plot the Flow."""
    click.echo("Plotting the Flow")
    plot_flow()


@flow.command(name="add-net")
@click.argument("crew_name")
def flow_add_crew(crew_name):
    """Add a net to an existing flow."""
    click.echo(f"Adding net {crew_name} to the flow")
    add_crew_to_flow(crew_name)


@magnet.command()
def chat():
    """
    Start a conversation with the Net, collecting user-supplied inputs,
    and using the Chat LLM to generate responses.
    """
    click.secho(
        "\nStarting a conversation with the Net\nType 'exit' or Ctrl+C to quit.\n",
    )

    run_chat()


@magnet.group(invoke_without_command=True)
def org():
    """Organization management commands."""


@org.command("list")
def org_list():
    """List available organizations."""
    org_command = OrganizationCommand()
    org_command.list()


@org.command()
@click.argument("id")
def switch(id):
    """Switch to a specific organization."""
    org_command = OrganizationCommand()
    org_command.switch(id)


@org.command()
def current():
    """Show current organization when 'magnet org' is called without subcommands."""
    org_command = OrganizationCommand()
    org_command.current()


@magnet.group()
def enterprise():
    """Enterprise Configuration commands."""


@enterprise.command("configure")
@click.argument("enterprise_url")
def enterprise_configure(enterprise_url: str):
    """Configure CrewAI Enterprise OAuth2 settings from the provided Enterprise URL."""
    enterprise_command = EnterpriseConfigureCommand()
    enterprise_command.configure(enterprise_url)


@magnet.group()
def config():
    """CLI Configuration commands."""


@config.command("list")
def config_list():
    """List all CLI configuration parameters."""
    config_command = SettingsCommand()
    config_command.list()


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str):
    """Set a CLI configuration parameter."""
    config_command = SettingsCommand()
    config_command.set(key, value)


@config.command("reset")
def config_reset():
    """Reset all CLI configuration parameters to default values."""
    config_command = SettingsCommand()
    config_command.reset_all_settings()


if __name__ == "__main__":
    magnet()
