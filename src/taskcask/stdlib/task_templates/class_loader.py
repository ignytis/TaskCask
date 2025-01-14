from typing import List, Type

from ...task_templates.class_loader import BaseTaskTemplateClassLoader
from ...task_templates.system_command import SystemCommandTaskTemplate


class ClassLoader(BaseTaskTemplateClassLoader):
    def load(self) -> List[Type]:
        return [SystemCommandTaskTemplate]
