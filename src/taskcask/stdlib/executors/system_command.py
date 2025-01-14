import subprocess

from ...executors.executor import BaseExecutor
from ...task_templates.task_template import BaseTaskTemplate
from ...task_templates.system_command import SystemCommandTaskTemplate


class SystemCommandExecutor(BaseExecutor):
    """
    Runs a system command with provided arguments
    """
    def supports_task_template(tpl: BaseTaskTemplate) -> bool:
        return isinstance(tpl, SystemCommandTaskTemplate)

    def execute(self, tpl: BaseTaskTemplate):
        tpl: SystemCommandTaskTemplate = tpl
        returned_value = subprocess.check_output(tpl.cmd, env=tpl.env).decode("utf-8")
        print(returned_value)
