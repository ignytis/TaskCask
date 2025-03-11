import logging
import subprocess
import shlex
from typing import Any

from ...stdlib.task_templates.system_command import SystemCommandTaskTemplate
from ..environments.enviromnent import DockerEnvironment, LocalEnvironment

from taskcask_common.environment import BaseEnvironment
from taskcask_common.executor import BaseExecutor
from taskcask_common.task import Task

_SUPPORTED_ENV_CLASSES = [DockerEnvironment, LocalEnvironment]


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


def _format_command(args: list[str]) -> str:
    """
    Formats a string command from list of strings
    """
    return " ".join(shlex.quote(arg) for arg in args)
