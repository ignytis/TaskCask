from typing import Generator
from abc import ABC

from ...config.types import Config
from ...typedefs import TaskTemplateDefinition


class BaseTaskTemplateDefinitionLoader(ABC):
    """
    Task template definition loaders implement different ways to load
    task template definitions: file formats, APIs, DBs, etc
    """
    def load(self, config: Config) -> Generator[dict[str, TaskTemplateDefinition], None, None]:
        raise NotImplementedError()
