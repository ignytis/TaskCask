from abc import ABC
from typing import Any

from ..task import Task
from ..environments.environment import BaseEnvironment


class BaseExecutor(ABC):
    """
    Executor is an object which run a specified task from template on particular environment
    """
    def can_execute(task: Task, env: BaseEnvironment) -> bool:
        raise NotImplementedError()

    def execute(self, task: Task, env: BaseEnvironment) -> Any:
        """
        Executes a task. If the task has any results, it should be returned to caller method
        in order to be printed or processed.
        """
        raise NotImplementedError()
