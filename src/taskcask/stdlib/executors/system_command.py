import subprocess

from ...executors.executor import BaseExecutor
from ...task import Task
from ...task_templates.task_template import BaseTaskTemplate
from ...task_templates.system_command import SystemCommandTaskTemplate


class SystemCommandExecutor(BaseExecutor):
    """
    Runs a system command with provided arguments
    """
    def supports_task_template(tpl: BaseTaskTemplate) -> bool:
        return isinstance(tpl, SystemCommandTaskTemplate)

    def execute(self, task: Task):
        tpl: SystemCommandTaskTemplate = task.template
        cmd = tpl.cmd + task.args
        returned_value = subprocess.check_output(cmd, env=tpl.env).decode("utf-8")
        print(returned_value)
