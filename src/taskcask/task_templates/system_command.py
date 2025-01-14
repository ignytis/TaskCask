from typing import Dict, List

from .task_template import BaseTaskTemplate


class SystemCommandTaskTemplate(BaseTaskTemplate):
    """A task template for system command"""
    kind: str = "system_command"
    cmd: List[str] = []
    env: Dict[str, str] = {}
