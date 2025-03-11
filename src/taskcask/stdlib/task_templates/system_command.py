from typing import Literal

from taskcask_common.task_template import BaseTaskTemplate
from taskcask_common.typedefs import StringKvDict


class SystemCommandTaskTemplate(BaseTaskTemplate):
    """A task template for system command"""
    kind: Literal["system_command"] = "system_command"
    cmd: list[str] = []
    env: StringKvDict = {}
