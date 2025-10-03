import subprocess

import click

from magnet.cli.utils import get_crews


def reset_memories_command(
    long,
    short,
    entity,
    knowledge,
    agent_knowledge,
    kickoff_outputs,
    all,
) -> None:
    """
    Reset the net memories.

    Args:
      long (bool): Whether to reset the long-term memory.
      short (bool): Whether to reset the short-term memory.
      entity (bool): Whether to reset the entity memory.
      kickoff_outputs (bool): Whether to reset the latest kickoff task outputs.
      all (bool): Whether to reset all memories.
      knowledge (bool): Whether to reset the knowledge.
      agent_knowledge (bool): Whether to reset the agents knowledge.
    """

    try:
        if not any([long, short, entity, kickoff_outputs, knowledge, agent_knowledge, all]):
            click.echo(
                "No memory type specified. Please specify at least one type to reset."
            )
            return

        crews = get_crews()
        if not crews:
            raise ValueError("No net found.")
        for net in crews:
            if all:
                net.reset_memories(command_type="all")
                click.echo(
                    f"[Net ({net.name if net.name else net.id})] Reset memories command has been completed."
                )
                continue
            if long:
                net.reset_memories(command_type="long")
                click.echo(
                    f"[Net ({net.name if net.name else net.id})] Long term memory has been reset."
                )
            if short:
                net.reset_memories(command_type="short")
                click.echo(
                    f"[Net ({net.name if net.name else net.id})] Short term memory has been reset."
                )
            if entity:
                net.reset_memories(command_type="entity")
                click.echo(
                    f"[Net ({net.name if net.name else net.id})] Entity memory has been reset."
                )
            if kickoff_outputs:
                net.reset_memories(command_type="kickoff_outputs")
                click.echo(
                    f"[Net ({net.name if net.name else net.id})] Latest Kickoff outputs stored has been reset."
                )
            if knowledge:
                net.reset_memories(command_type="knowledge")
                click.echo(
                    f"[Net ({net.name if net.name else net.id})] Knowledge has been reset."
                )
            if agent_knowledge:
                net.reset_memories(command_type="agent_knowledge")
                click.echo(
                    f"[Net ({net.name if net.name else net.id})] Agents knowledge has been reset."
                )

    except subprocess.CalledProcessError as e:
        click.echo(f"An error occurred while resetting the memories: {e}", err=True)
        click.echo(e.output, err=True)

    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
