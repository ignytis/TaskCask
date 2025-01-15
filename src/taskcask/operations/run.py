import logging
from typing import List

from ..executors.executor import BaseExecutor
from ..executors.factory import get_executor_classes
from ..task_templates.factory import get_task_template_from_dict

log = logging.getLogger(__name__)


def run(target: str, args: List[str]) -> None:
    """
    Runs a command.

    Parameters:
        target (str): task template ID + optional execution environment separated with '@'
        args (List[str]): task arguments
    """
    log.info("Running a command...")

    target_list = target.split("@")
    task_template_id = target_list[0]
    target_env = target_list[1] if len(target_list) > 1 else None


    task_def = {
        "kind": "system_command",
        "cmd": ["bash", "-c", "echo \"Hello, World! $APP\""],
        "env": {
            "APP": "hello"
        }
    }
    task_tpl = get_task_template_from_dict(task_def)

    executor: BaseExecutor | None = None
    for executor_cls in get_executor_classes():
        if executor_cls.supports_task_template(task_tpl):
            executor = executor_cls()
            break

    if not executor:
        raise Exception("No appropriate executor found. The task was not executed.")

    executor.execute(task_tpl)
