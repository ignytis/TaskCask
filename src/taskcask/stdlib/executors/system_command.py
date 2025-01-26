import subprocess

from ...environments.environment import BaseEnvironment
from ...executors.executor import BaseExecutor
from ...task import Task
from ...stdlib.task_templates.system_command import SystemCommandTaskTemplate
from ..environments.enviromnent import LocalEnvironment


class SystemCommandExecutor(BaseExecutor):
    """
    Runs a system command with provided arguments
    """
    def can_execute(task: Task, env: BaseEnvironment) -> bool:
        return isinstance(task.template, SystemCommandTaskTemplate) \
            and isinstance(env, LocalEnvironment)

    def execute(self, task: Task, env: BaseEnvironment):
        if not isinstance(env, LocalEnvironment):
            raise Exception(f"Unsupported target environment: {env.kind}")
        tpl: SystemCommandTaskTemplate = task.template
        cmd = tpl.cmd + task.args
        env = {**env.env, **tpl.env}
        returned_value = subprocess.check_output(cmd, env=env).decode("utf-8")
        print(returned_value)
