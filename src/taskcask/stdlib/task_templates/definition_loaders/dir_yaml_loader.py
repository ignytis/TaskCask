import logging
from pathlib import Path
from typing import Generator

from pydantic import BaseModel

from ....config.types import Config
from ....task_templates.definitions.loader import BaseTaskTemplateDefinitionLoader
from ....typedefs import TaskTemplateDefinition


class LoaderConfig(BaseModel):
    path: str


class Loader(BaseTaskTemplateDefinitionLoader):
    log = logging.getLogger(__name__)

    """
    Loads task template definitions from YAML files by reading provided directories recursively
    """
    def load(self, config: Config) -> Generator[dict[str, TaskTemplateDefinition], None, None]:
        try:
            import yaml
        except ModuleNotFoundError:
            self.log.warning("PyYAML is not installed. "
                             "Please install the application with 'yaml' extra to use YAML configuration")
            return

        loader_cfg = LoaderConfig.model_validate(config.task_template_loaders.get("dir_yaml"))
        for loader_cfg_path in loader_cfg.path.split(":"):
            for path in Path(loader_cfg_path).rglob('*.yaml'):
                with open(path) as f:
                    yield yaml.load(f, Loader=yaml.loader.FullLoader)
