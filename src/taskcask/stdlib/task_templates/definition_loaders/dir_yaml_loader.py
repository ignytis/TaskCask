import logging
from pathlib import Path
from typing import Generator

from ....task_templates.definitions.loader import BaseTaskTemplateDefinitionLoader
from ....typedefs import TaskTemplateDefinition


class Loader(BaseTaskTemplateDefinitionLoader):
    log = logging.getLogger(__name__)

    """
    Loads task template definitions from YAML files by reading provided directories recursively
    """
    def load(self) -> Generator[dict[str, TaskTemplateDefinition], None, None]:
        try:
            import yaml
        except ModuleNotFoundError:
            self.log.warning("PyYAML is not installed. "
                             "Please install the application with 'yaml' extra to use YAML configuration")
            return

        for path in Path('examples/task_templates').rglob('*.yaml'):
            with open(path) as f:
                yield yaml.load(f, Loader=yaml.loader.FullLoader)
