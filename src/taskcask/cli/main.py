import click

from .commands.run import cmd_run
from .commands.config import cmd_config


@click.group
def cmd_group_main() -> None:
    pass


cmd_group_main.add_command(cmd_config)
cmd_group_main.add_command(cmd_run)


if __name__ == "__main__":
    cmd_group_main()
