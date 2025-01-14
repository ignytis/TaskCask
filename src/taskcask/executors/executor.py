from abc import ABC

from ..task_templates.task_template import BaseTaskTemplate


class BaseExecutor(ABC):
    def supports_task_template(tpl: BaseTaskTemplate) -> bool:
        raise NotImplementedError()

    def execute(self, tpl: BaseTaskTemplate) -> None:
        raise NotImplementedError()
