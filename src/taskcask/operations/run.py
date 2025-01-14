import logging
from typing import List

from ..executors.factory import get_executor_classes
from ..task_templates.factory import get_task_template_from_dict

log = logging.getLogger(__name__)


def run(ask_template_id: str, param: List[str]) -> None:
    log.info("Running a command...")

    task_def = {
        "kind": "system_command",
        "cmd": ["echo", "Hello, World!", *param],
        "env": {
            "APP": "hello"
        }
    }
    task_tpl = get_task_template_from_dict(task_def)

    is_executed = False
    for executor_cls in get_executor_classes():
        if not executor_cls.supports_task_template(task_tpl):
            continue
        executor = executor_cls()
        executor.execute(task_tpl)
        is_executed = True

    if not is_executed:
        raise Exception("No appropriate executor found. The task was not executed.")
