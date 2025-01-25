import click

from ...config.compiler import compile_config
from ...operations.run import run


@click.command(name="run", help="Runs a command. Target is a task template ID and "
               "optional execution environment separaterd with '@'")
@click.option("--param", "-p", "params", multiple=True, default=[],
              help="Parameter overrides. Can be specified multiple times")
@click.argument("target")
@click.argument("args", nargs=-1)
def cmd_run(target: str, params: list[str], args: tuple[str]) -> None:
    config = compile_config(params)
    run(target, config, args)
