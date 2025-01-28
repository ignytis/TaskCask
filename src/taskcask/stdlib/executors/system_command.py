import logging
import subprocess

from ...environments.environment import BaseEnvironment
from ...executors.executor import BaseExecutor
from ...task import Task
from ...stdlib.task_templates.system_command import SystemCommandTaskTemplate
from ..environments.enviromnent import LocalEnvironment, SshEnvironment


def _is_supported_env(env: BaseEnvironment) -> bool:
    return isinstance(env, LocalEnvironment) or isinstance(env, SshEnvironment)


class SystemCommandExecutor(BaseExecutor):
    """
    Runs a system command with provided arguments
    """
    log = logging.getLogger(__name__)

    def can_execute(task: Task, env: BaseEnvironment) -> bool:
        return isinstance(task.template, SystemCommandTaskTemplate) \
            and _is_supported_env(env)

    def execute(self, task: Task, env: BaseEnvironment):
        if isinstance(env, LocalEnvironment):
            return self._run_locally(task, env)
        elif isinstance(env, SshEnvironment):
            return self._run_ssh(task, env)
        else:
            raise Exception(f"Unsupported target environment: {env.kind}")

    def _run_locally(self, task: Task, env: LocalEnvironment):
        tpl: SystemCommandTaskTemplate = task.template
        cmd = tpl.cmd + task.args
        env_dict = {**env.env, **tpl.env}
        returned_value = subprocess.check_output(cmd, env=env_dict).decode("utf-8")
        print(returned_value)

    def _run_ssh(self, task: Task, env: SshEnvironment):
        try:
            from fabric import Connection
        except ImportError:
            self.log.error("Cannot import Fabric. Please install the application with 'ssh' extra")
            return

        tpl: SystemCommandTaskTemplate = task.template
        cmd = tpl.cmd + task.args
        env_dict = {**env.env, **tpl.env}
        command_string = " ".join(['"'+part+'"' if " " in part else part for part in cmd])

        with Connection(env.host, user=env.user, port=env.port) as c:
            result = c.run(command_string, hide=True, env=env_dict)
        print(result.stdout)
