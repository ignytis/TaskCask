from datetime import datetime
import logging
import os.path
from pathlib import Path
from typing import Any, Generator

import jinja2
import yaml

from ..config.types import Config
from ..environments.environment import BaseEnvironment
from ..executors.executor import BaseExecutor
from ..task import Task
from ..task_templates.task_template import BaseTaskTemplate
from ..task_templates.factory import get_task_template_from_dict
from ..typedefs import TaskTemplateDefinition
from ..utils.reflection import get_all_subclasses


log = logging.getLogger(__name__)


def run(target: str, config: Config, args: list[str]) -> None:
    """
    Runs a command.

    Parameters:
        target (str): task template ID + optional execution environment separated with '@'
        args (list[str]): task arguments
    """
    log.info("Running a command...")

    if target.count("@") > 1:
        raise ValueError("Too many '@' characters in target."
                         "The correct format is: task_template_id[@target_environment]")
    elif "@" not in target:
        target += "@"
    [task_template_id, target_env] = target.split("@")
    target_env = _get_target_env(config, target_env)

    task_tpl = _get_task_template(config, task_template_id)
    task = Task(
        template=task_tpl,
        args=args,
    )
    executor = _get_executor(task, target_env)

    task.execution_start = datetime.now()
    result: Any = executor.execute(task, target_env)
    print_result = config.io.print_result if task.template.print_result is None else task.template.print_result
    if print_result:
        print(result)
    task.execution_end = datetime.now()
    log.info("Execution started at {} and finished at {}. Time elapsed: {}"
             .format(task.execution_start, task.execution_start, task.execution_end - task.execution_start))


def _get_task_template(config: Config, task_template_id: str) -> BaseTaskTemplate:
    task_tpl_def: TaskTemplateDefinition | None = None
    for _task_tpl_defs in _get_task_template_definitions(config):
        if task_template_id in _task_tpl_defs:
            task_tpl_def = _task_tpl_defs[task_template_id]
            break
    if not task_tpl_def:
        raise Exception(f"Cannot find a task template definition with ID '{task_template_id}'")

    return get_task_template_from_dict(task_tpl_def)


def _get_executor(task: Task, env: BaseEnvironment) -> BaseExecutor:
    executor: BaseExecutor | None = None
    for executor_cls in get_all_subclasses(BaseExecutor):
        if executor_cls.can_execute(task, env):
            executor = executor_cls()
            break

    if not executor:
        raise Exception("No appropriate executor found. The task was not executed.")

    return executor


def _get_target_env(config: Config, target_env: str | None = None) -> BaseEnvironment:
    if not target_env:
        target_env = "local"

    env = config.environments.get(target_env)
    if env is None:
        if "local" != target_env:
            raise ValueError(f"Environment '{target_env}' not found in configuration.")
        # Instead of requiring the local config in config, create a basic local env
        env = {"kind": "local"}

    return BaseEnvironment.create_from_dict(env)


def _get_task_template_definitions(config: Config) -> Generator[dict[str, TaskTemplateDefinition], None, None]:
    """
    Generates the dictionaries of task template definitions (which are dicrionaties of task template attributes).
    Keys are task template identifiers.
    """
    for loader_cfg_path in config.task_templates.lookup_dirs:
        for task_def_tpl_path in Path(loader_cfg_path).rglob("*.yaml.jinja2"):
            cfg_dir = os.path.dirname(task_def_tpl_path)
            task_def_tpl_filename = os.path.basename(task_def_tpl_path)
            # TODO: make common base environment with task templates
            jinja_env = jinja2.Environment(undefined=jinja2.StrictUndefined, loader=jinja2.FileSystemLoader(cfg_dir))
            tpl = jinja_env.get_template(task_def_tpl_filename)
            yield yaml.load(tpl.render({"cfg": config, "params": config.params}), Loader=yaml.FullLoader)
