import importlib
import logging

from ...environments.environment import BaseEnvironment
from ...executors.executor import BaseExecutor
from ...task import Task
from ..task_templates.python import PythonTaskTemplate
from ..environments.enviromnent import LocalEnvironment


class PythonExecutor(BaseExecutor):
    """
    Runs a python script
    """
    log = logging.getLogger(__name__)

    def can_execute(task: Task, env: BaseEnvironment) -> bool:
        return isinstance(task.template, PythonTaskTemplate) \
            and isinstance(env, LocalEnvironment)

    def execute(self, task: Task, env: LocalEnvironment):
        tpl: PythonTaskTemplate = task.template

        module_path, function_name = tpl.module_path.rsplit(":", 1)
        module = importlib.import_module(module_path)
        function = getattr(module, function_name)

        print(function(*tpl.args, **tpl.kwargs))
