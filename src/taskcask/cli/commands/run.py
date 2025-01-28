import click

from ...operations.run import run
from ...app import app_get_config


@click.command(name="run", help="Runs a command. Target is a task template ID and "
               "optional execution environment separaterd with '@'")
@click.option("--param", "-p", "params", multiple=True, default=[],
              help="Parameter overrides. Can be specified multiple times")
@click.argument("target")
@click.argument("args", nargs=-1)
def cmd_run(target: str, params: list[str], args: list[str]) -> None:
    run(target, app_get_config(params), args)
