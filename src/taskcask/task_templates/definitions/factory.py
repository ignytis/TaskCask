from typing import Generator

from ...config.types import Config
from .loader import BaseTaskTemplateDefinitionLoader
from ...typedefs import TaskTemplateDefinition
from ...utils.reflection import get_all_subclasses


def get_task_template_definitions(config: Config) -> Generator[dict[str, TaskTemplateDefinition], None, None]:
    for cls in get_all_subclasses(BaseTaskTemplateDefinitionLoader):
        for d in cls().load(config) or []:
            yield d
