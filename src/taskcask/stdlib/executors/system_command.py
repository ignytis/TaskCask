import logging
import subprocess
import shlex
from typing import Any

from ...environments.environment import BaseEnvironment
from ...executors.executor import BaseExecutor
from ...task import Task
from ...stdlib.task_templates.system_command import SystemCommandTaskTemplate
from ..environments.enviromnent import DockerEnvironment, LocalEnvironment, SshEnvironment


_SUPPORTED_ENV_CLASSES = [DockerEnvironment, LocalEnvironment, SshEnvironment]


def _is_supported_env(env: BaseEnvironment) -> bool:
    for cls in _SUPPORTED_ENV_CLASSES:
        if isinstance(env, cls):
            return True
    return False


class SystemCommandExecutor(BaseExecutor):
    """
    Runs a system command with provided arguments
    """
    log = logging.getLogger(__name__)

    def can_execute(task: Task, env: BaseEnvironment) -> bool:
        return isinstance(task.template, SystemCommandTaskTemplate) \
            and _is_supported_env(env)

    def execute(self, task: Task, env: BaseEnvironment) -> Any:
        if isinstance(env, DockerEnvironment):
            return self._run_docker(task, env)
        elif isinstance(env, LocalEnvironment):
            return self._run_locally(task, env)
        elif isinstance(env, SshEnvironment):
            return self._run_ssh(task, env)
        else:
            raise NotImplementedError(f"Unsupported target environment: {env.kind}")

    def _run_docker(self, task: Task, env: DockerEnvironment):
        """
        Run a system command in Docker containers
        """
        try:
            import docker
        except ImportError:
            raise Exception("Cannot import Docker. Please install the application with 'docker' extra")
        tpl: SystemCommandTaskTemplate = task.template
        cmd = tpl.cmd + task.args
        env_dict = {**env.env, **tpl.env}
        command_string = _format_command(cmd)

        client = docker.from_env()
        return client.containers.run(image=env.image, command=command_string, entrypoint=None, environment=env_dict) \
            .decode("utf-8")

    def _run_locally(self, task: Task, env: LocalEnvironment):
        """
        Run a system command as a local process
        """
        tpl: SystemCommandTaskTemplate = task.template
        cmd = tpl.cmd + task.args
        env_dict = {**env.env, **tpl.env}
        return subprocess.check_output(cmd, env=env_dict).decode("utf-8")

    def _run_ssh(self, task: Task, env: SshEnvironment):
        """
        Run a system command on a remove server using SSH
        """
        try:
            from fabric import Connection
        except ImportError:
            raise Exception("Cannot import Fabric. Please install the application with 'ssh' extra")

        tpl: SystemCommandTaskTemplate = task.template
        cmd = tpl.cmd + task.args
        env_dict = {**env.env, **tpl.env}
        command_string = " ".join(['"'+part+'"' if " " in part else part for part in cmd])

        with Connection(env.host, user=env.user, port=env.port) as c:
            result = c.run(command_string, hide=True, env=env_dict)
        return result.stdout


def _format_command(args: list[str]) -> str:
    """
    Formats a string command from list of strings
    """
    return " ".join(shlex.quote(arg) for arg in args)
