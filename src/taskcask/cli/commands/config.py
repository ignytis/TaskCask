import click

from ...app import app_get_config


@click.command(name="config", help="Prints configuration")
@click.option("--param", "-p", "params", multiple=True, default=[],
              help="Parameter overrides. Can be specified multiple times")
def cmd_config(params: list[str]) -> None:
    config = app_get_config(params)
    print(config.model_dump_json(indent=2))
