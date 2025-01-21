import click

from ...config.types import Config
from .decorators.taskcask_command import taskcask_command
from ...operations.run import run


@click.command(name="run", help="Runs a command. Target is a task template ID and "
               "optional execution environment separaterd with '@'")
@click.argument("target")
@click.argument('args', nargs=-1)
@taskcask_command
def cmd_run(target: str, args: list[str], config: Config) -> None:
    """
    Runs a command with provided arguments
    """
    run(target, config, args)
