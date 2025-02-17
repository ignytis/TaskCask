import click

from ...app import app_get_config

from ...task_templates.loader import get_task_template_definitions


@click.command(name="list", help="Lists the task templates")
@click.option("--param", "-p", "params", multiple=True, default=[],
              help="Parameter overrides. Can be specified multiple times")
def cmd_list(params: list[str]) -> None:
    cfg = app_get_config(params)
    tpls = []
    for task_group in get_task_template_definitions(cfg):
        for task_template_id in task_group:
            tpls.append(task_template_id)
    tpls.sort()
    for t in tpls:
        print(t)
