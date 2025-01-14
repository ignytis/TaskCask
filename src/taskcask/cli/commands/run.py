import click

from ...operations.run import run


@click.command(name="run", help="Runs a command")
@click.argument("task_template_id")
@click.argument('args', nargs=-1)
def cmd_run(task_template_id: str, args) -> None:
    """
    Runs a command with provided arguments
    """
    run(task_template_id, args)
