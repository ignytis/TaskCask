from pathlib import Path
from typing import Generator

from ....task_templates.definitions.loader import BaseTaskTemplateDefinitionLoader
from ....typedefs import TaskTemplateDefinition


class Loader(BaseTaskTemplateDefinitionLoader):
    def load(self) -> Generator[dict[str, TaskTemplateDefinition], None, None]:
        try:
            import yaml
        except ModuleNotFoundError:
            return

        for path in Path('examples/task_templates').rglob('*.yaml'):
            with open(path) as f:
                yield yaml.load(f, Loader=yaml.loader.FullLoader)
