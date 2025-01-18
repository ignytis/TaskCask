from importlib.metadata import entry_points
from typing import Generator, Type


from .loader import BaseTaskTemplateDefinitionLoader
from ...typedefs import TaskTemplateDefinition


def get_task_template_definitions() -> Generator[dict[str, TaskTemplateDefinition], None, None]:
    for entry_point in entry_points(group="taskcask.task_templates.definition_loaders"):
        cls: Type[BaseTaskTemplateDefinitionLoader] = entry_point.load()
        for d in cls().load() or []:
            yield d
