from typing import Type

from ...task_templates.class_loader import BaseTaskTemplateClassLoader
from ...task_templates.system_command import SystemCommandTaskTemplate


class ClassLoader(BaseTaskTemplateClassLoader):
    def load(self) -> list[Type]:
        return [SystemCommandTaskTemplate]
