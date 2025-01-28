from typing import Literal

from ...task_templates.task_template import BaseTaskTemplate


class PythonTaskTemplate(BaseTaskTemplate):
    """A task template for Python script"""
    kind: Literal["python"] = "python"
    module_path: str | None = None
    """e.g. my_module.my_sub_module:my_function"""
    args: list = []
    kwargs: dict = {}
