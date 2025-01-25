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

    def execute(self, tpl: BaseTaskTemplate, args: list[str] | None = None):
        if args is None:
            args = []
        tpl: SystemCommandTaskTemplate = tpl
        cmd = tpl.cmd + args
        returned_value = subprocess.check_output(cmd, env=tpl.env).decode("utf-8")
        print(returned_value)
