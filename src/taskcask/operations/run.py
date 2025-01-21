import logging

from ..config.types import Config
from ..executors.executor import BaseExecutor
from ..executors.factory import get_executor_classes
from ..task_templates.class_factory import get_task_template_from_dict
from ..task_templates.definitions.factory import get_task_template_definitions
from ..typedefs import TaskTemplateDefinition

log = logging.getLogger(__name__)


def run(target: str, config: Config, args: list[str]) -> None:
    """
    Runs a command.

    Parameters:
        target (str): task template ID + optional execution environment separated with '@'
        args (list[str]): task arguments
    """
    log.info("Running a command...")

    target_list = target.split("@")
    task_template_id = target_list[0]
    target_env = target_list[1] if len(target_list) > 1 else None

    task_tpl_def: TaskTemplateDefinition | None = None
    for _task_tpl_defs in get_task_template_definitions(config):
        if task_template_id in _task_tpl_defs:
            task_tpl_def = _task_tpl_defs[task_template_id]
            break
    if not task_tpl_def:
        raise Exception(f"Cannot find a task template definition with ID '{task_template_id}'")

    task_tpl = get_task_template_from_dict(task_tpl_def)

    executor: BaseExecutor | None = None
    for executor_cls in get_executor_classes():
        if executor_cls.supports_task_template(task_tpl):
            executor = executor_cls()
            break

    if not executor:
        raise Exception("No appropriate executor found. The task was not executed.")

    executor.execute(task_tpl)
