from typing import Generator, Type
from pkg_resources import iter_entry_points

from .loader import BaseTaskTemplateDefinitionLoader
from ...typedefs import TaskTemplateDefinition


def get_task_template_definitions() -> Generator[dict[str, TaskTemplateDefinition], None, None]:
    for entry_point in iter_entry_points("taskcask.task_templates.definition_loaders"):
        cls: Type[BaseTaskTemplateDefinitionLoader] = entry_point.load()
        for d in cls().load() or []:
            yield d
