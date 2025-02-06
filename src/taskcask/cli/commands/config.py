import click
import yaml

from ...app import app_get_config


@click.command(name="config", help="Prints configuration")
@click.option("--param", "-p", "params", multiple=True, default=[],
              help="Parameter overrides. Can be specified multiple times")
@click.option("--format", "-f", type=click.Choice(["yaml", "json"], case_sensitive=False), default="yaml")
def cmd_config(params: list[str], format: str) -> None:
    config = app_get_config(params)
    output: str | None = None
    if "json" == format:
        output = config.model_dump_json(indent=2)
    elif "yaml" == format:
        output = yaml.dump(config.model_dump())
    else:
        raise ValueError(f"Invalid format: {format}")
    print(output)
