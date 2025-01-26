import click

from ...autoloader import load_plugins
from ...config.compiler import compile_config


@click.command(name="config", help="Prints configuration")
@click.option("--param", "-p", "params", multiple=True, default=[],
              help="Parameter overrides. Can be specified multiple times")
def cmd_config(params: list[str]) -> None:
    load_plugins()
    config = compile_config(params)
    print(config.model_dump_json(indent=2))
