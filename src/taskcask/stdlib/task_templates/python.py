from typing import Literal

from ...task_templates.task_template import BaseTaskTemplate


class PythonTaskTemplate(BaseTaskTemplate):
    """A task template for Python script"""
    kind: Literal["python"] = "python"

    module_path: str | None = None
    """Module path to Python callable e.g. my_lib.my_module:my_fn"""
    file_path: str | None = None
    """Path to Python file"""

    args: list = []
    kwargs: dict = {}
