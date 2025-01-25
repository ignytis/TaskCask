from abc import ABC

from ..task_templates.task_template import BaseTaskTemplate


class BaseExecutor(ABC):
    """
    Executor is an object which run a specified task from template on particular environment
    """
    def supports_task_template(tpl: BaseTaskTemplate) -> bool:
        raise NotImplementedError()

    def execute(self, tpl: BaseTaskTemplate, args: list[str] | None = None) -> None:
        raise NotImplementedError()
