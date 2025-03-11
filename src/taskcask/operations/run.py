import logging

from ..config.types import Config
from ..task_templates.loader import get_task_template_definitions
from ..task_templates.factory import get_task_template_from_dict
from taskcask_common.utils.reflection import get_all_subclasses

from taskcask_common.environment import BaseEnvironment
from taskcask_common.events import listeners
from taskcask_common.events import types as event_types
from taskcask_common.executor import BaseExecutor
from taskcask_common.task import Task
from taskcask_common.task_template import BaseTaskTemplate

from taskcask_common.typedefs import TaskTemplateDefinition

log = logging.getLogger(__name__)


def run(target: str, config: Config, args: list[str]) -> None:
    """
    Runs a command.

    Parameters:
        target (str): task template ID + optional execution environment separated with '@'
        args (list[str]): task arguments
    """
    log.info("Running a command...")

    listeners.BaseTaskPreExecuteListener.register_listeners()
    listeners.BaseTaskPostExecuteListener.register_listeners()
    listeners.BaseGetTargetEnvironmentListener.register_listeners()

    if target.count("@") > 1:
        raise ValueError("Too many '@' characters in target."
                         "The correct format is: task_template_id[@target_environment]")
    elif "@" not in target:
        target += "@"
    [task_template_id, target_env] = target.split("@")

    task_tpl = _get_task_template(config, task_template_id)
    task = Task(
        template=task_tpl,
        args=args,
    )
    target_env = _get_target_env(config, task, target_env)
    executor = _get_executor(task, target_env)

    listeners.BaseTaskPreExecuteListener.process_event(event_types.PreExecuteEvent(environment=target_env, task=task))
    log.info(f"Executing a task '{task.id}' from template '{task.template.id}'...")
    task.result = executor.execute(task, target_env)
    listeners.BaseTaskPostExecuteListener.process_event(event_types.PostExecuteEvent(environment=target_env, task=task))

    print_result = config.io.print_result if task.template.print_result is None else task.template.print_result
    if print_result:
        print(task.result)


def _get_task_template(config: Config, task_template_id: str) -> BaseTaskTemplate:
    task_tpl_def: TaskTemplateDefinition | None = None
    for _task_tpl_defs in get_task_template_definitions(config):
        if task_template_id in _task_tpl_defs:
            task_tpl_def = _task_tpl_defs[task_template_id]
            break
    if not task_tpl_def:
        raise Exception(f"Cannot find a task template definition with ID '{task_template_id}'")

    return get_task_template_from_dict(task_tpl_def, task_template_id)


def _get_executor(task: Task, env: BaseEnvironment) -> BaseExecutor:
    executor: BaseExecutor | None = None
    for executor_cls in get_all_subclasses(BaseExecutor):
        if executor_cls.can_execute(task, env):
            executor = executor_cls()
            break

    if not executor:
        raise Exception("No appropriate executor found. The task was not executed.")

    return executor


def _get_target_env(config: Config, task: Task, target_env: str | None = None) -> BaseEnvironment:
    event = event_types.GetTargetEnvironmentEvent(task=task, target_env=target_env)
    listeners.BaseGetTargetEnvironmentListener.process_event(event)
    target_env = event.target_env

    if not target_env:
        target_env = "local"

    env = config.environments.get(target_env)
    if env is None:
        if "local" != target_env:
            raise ValueError(f"Environment '{target_env}' not found in configuration.")
        # Instead of requiring the local config in config, create a basic local env
        env = {"kind": "local"}

    return BaseEnvironment.create_from_dict(env)
