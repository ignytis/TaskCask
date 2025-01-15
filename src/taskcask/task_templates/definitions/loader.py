from typing import Generator
from abc import ABC

from ...typedefs import TaskTemplateDefinition


class BaseTaskTemplateDefinitionLoader(ABC):
    """
    Task template definition loaders implement different ways to load
    task template definitions: file formats, APIs, DBs, etc
    """
    def load(self) -> Generator[dict[str, TaskTemplateDefinition], None, None]:
        raise NotImplementedError()
