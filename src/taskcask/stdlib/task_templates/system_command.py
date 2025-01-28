from typing import Literal

from ...task_templates.task_template import BaseTaskTemplate
from ...typedefs import StringKvDict


class SystemCommandTaskTemplate(BaseTaskTemplate):
    """A task template for system command"""
    kind: Literal["system_command"] = "system_command"
    cmd: list[str] = []
    env: StringKvDict = {}
