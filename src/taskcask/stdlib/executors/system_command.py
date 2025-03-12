import logging
import subprocess
from typing import Any

from ..environments.enviromnent import LocalEnvironment

from taskcask_common.environment import BaseEnvironment
from taskcask_common.executor import BaseExecutor
from taskcask_common.task import Task
from taskcask_common.task_templates.system_command import SystemCommandTaskTemplate


class SystemCommandExecutor(BaseExecutor):
    """
    Runs a system command with provided arguments
    """
    log = logging.getLogger(__name__)

    def can_execute(task: Task, env: BaseEnvironment) -> bool:
        return isinstance(task.template, SystemCommandTaskTemplate) \
            and isinstance(env, LocalEnvironment)

    def execute(self, task: Task, env: BaseEnvironment) -> Any:
        tpl: SystemCommandTaskTemplate = task.template
        cmd = tpl.cmd + task.args
        env_dict = {**env.env, **tpl.env}
        return subprocess.check_output(cmd, env=env_dict).decode("utf-8")
