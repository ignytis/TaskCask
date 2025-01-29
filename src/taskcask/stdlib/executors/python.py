import importlib
import importlib.util
import io
import logging

from ...environments.environment import BaseEnvironment
from ...executors.executor import BaseExecutor
from ...task import Task
from ..task_templates.python import PythonTaskTemplate
from ..environments.enviromnent import LocalEnvironment, SshEnvironment


def _is_supported_env(env: BaseEnvironment) -> bool:
    return isinstance(env, LocalEnvironment) or isinstance(env, SshEnvironment)


class PythonExecutor(BaseExecutor):
    """
    Runs a python script
    """
    log = logging.getLogger(__name__)

    def can_execute(task: Task, env: BaseEnvironment) -> bool:
        return isinstance(task.template, PythonTaskTemplate) \
            and _is_supported_env(env)

    def execute(self, task: Task, env: BaseEnvironment):
        tpl: PythonTaskTemplate = task.template

        # TODO: make mutually exclusive
        if tpl.module_path is not None:
            module_path, function_name = tpl.module_path.rsplit(":", 1)
            module = importlib.import_module(module_path)
        elif tpl.file_path:
            module_path, function_name = tpl.file_path.rsplit(":", 1)
            spec = importlib.util.spec_from_file_location("my_module", module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        if isinstance(env, LocalEnvironment):
            function = getattr(module, function_name)
            result = function(*tpl.args, **tpl.kwargs)

            # TODO: parametrize
            print(result)
        elif isinstance(env, SshEnvironment):
            try:
                from fabric import Connection
            except ImportError:
                self.log.error("Cannot import Fabric. Please install the application with 'ssh' extra")
                return

            with open(module.__file__, "r") as f:
                py_code = f.read()
            fn_signature = _format_function_signature(tpl.args, tpl.kwargs)
            py_code += f"\n{function_name}({fn_signature})"
            py_code = io.StringIO(py_code)
            with Connection(env.host, user=env.user, port=env.port) as c:
                result = c.run("python -", hide=True, env=env.env, in_stream=py_code)
            print(result.stdout)


def _format_function_signature(py_args: list, py_kwargs: dict) -> str:
    """
    Converts Python args and kwargs into string representations parseable inside scripts.
    Works with simple types and collections only
    """
    args_str = ", ".join(map(repr, py_args))
    kwargs_str = ", ".join(f"{k}={repr(v)}" for k, v in py_kwargs.items())
    if args_str and kwargs_str:
        return f"{args_str}, {kwargs_str}"
    elif args_str:
        return args_str
    elif kwargs_str:
        return kwargs_str
    else:
        return ""
