import click

from .commands.config import cmd_config
from .commands.list import cmd_list
from .commands.run import cmd_run


@click.group
def cmd_group_main() -> None:
    pass


cmd_group_main.add_command(cmd_run)
cmd_group_main.add_command(cmd_list)
cmd_group_main.add_command(cmd_config)


if __name__ == "__main__":
    cmd_group_main()
