from typing import Literal, Self

from pydantic import model_validator

from taskcask_common.task_template import BaseTaskTemplate


class PythonTaskTemplate(BaseTaskTemplate):
    """A task template for Python script"""
    kind: Literal["python"] = "python"

    module_path: str | None = None
    """Module path to Python callable e.g. my_lib.my_module:my_fn"""
    file_path: str | None = None
    """Path to Python file"""

    args: list = []
    kwargs: dict = {}

    @model_validator(mode="after")
    def path_xor(self) -> Self:
        if bool(self.module_path) == bool(self.file_path):
            raise ValueError("Exactly one parameter must be specified: either file_path or module path")
        return self
