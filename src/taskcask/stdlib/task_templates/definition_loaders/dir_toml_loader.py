import logging
from pathlib import Path
import tomllib
from typing import Generator

from pydantic import BaseModel

from ....config.types import Config
from ....task_templates.definitions.loader import BaseTaskTemplateDefinitionLoader
from ....typedefs import TaskTemplateDefinition


class LoaderConfig(BaseModel):
    enabled: bool = True
    path: str


class Loader(BaseTaskTemplateDefinitionLoader):
    log = logging.getLogger(__name__)

    """
    Loads task template definitions from TOML files by reading provided directories recursively
    """
    def load(self, config: Config) -> Generator[dict[str, TaskTemplateDefinition], None, None]:
        loader_cfg = LoaderConfig.model_validate(config.task_template_loaders.get("dir_toml"))
        if not loader_cfg.enabled:
            return
        for loader_cfg_path in loader_cfg.path.split(":"):
            for path in Path(loader_cfg_path).rglob("*.toml"):
                with open(path, "rb") as f:
                    yield tomllib.load(f)
