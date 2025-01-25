from datetime import datetime
import logging

from ..config.types import Config
from ..executors.executor import BaseExecutor
from ..executors.factory import get_executor_classes
from ..task import Task
from ..task_templates.task_template import BaseTaskTemplate
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

    if target.count("@") > 1:
        raise ValueError("Too many '@' characters in target."
                         "The correct format is: task_template_id[@target_environment]")
    elif "@" not in target:
        target += "@"
    [task_template_id, target_env] = target.split("@")
    # TODO: implement
    # TODO: add validation. Alphanumeric characters, .-_ for both

    task_tpl = _get_task_template(config, task_template_id)
    task = Task(
        template=task_tpl,
        args=args,
    )
    executor = _get_executor(task_tpl)

    task.execution_start = datetime.now()
    executor.execute(task)
    task.execution_end = datetime.now()
    log.info("Execution started at {} and finished at {}. Time elapsed: {}"
             .format(task.execution_start, task.execution_start, task.execution_end - task.execution_start))


def _get_task_template(config: Config, task_template_id: str) -> BaseTaskTemplate:
    task_tpl_def: TaskTemplateDefinition | None = None
    for _task_tpl_defs in get_task_template_definitions(config):
        if task_template_id in _task_tpl_defs:
            task_tpl_def = _task_tpl_defs[task_template_id]
            break
    if not task_tpl_def:
        raise Exception(f"Cannot find a task template definition with ID '{task_template_id}'")

    return get_task_template_from_dict(task_tpl_def)


def _get_executor(task_tpl: BaseTaskTemplate) -> BaseExecutor:
    executor: BaseExecutor | None = None
    for executor_cls in get_executor_classes():
        if executor_cls.supports_task_template(task_tpl):
            executor = executor_cls()
            break

    if not executor:
        raise Exception("No appropriate executor found. The task was not executed.")

    return executor
