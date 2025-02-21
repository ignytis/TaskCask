from pathlib import Path
from typing import Generator

import yaml

from ..config.types import Config
from ..utils.jinja import jinja_render_from_file
from ..typedefs import TaskTemplateDefinition


def get_task_template_definitions(config: Config) -> Generator[dict[str, TaskTemplateDefinition], None, None]:
    """
    Generates the dictionaries of task template definitions (which are dicrionaties of task template attributes).
    Keys are task template identifiers.
    """
    for loader_cfg_path in config.task_templates.lookup_dirs:
        for task_def_tpl_path in Path(loader_cfg_path).rglob("*.tcask"):
            yield yaml.load(jinja_render_from_file(task_def_tpl_path, {"cfg": config, "params": config.params}),
                            Loader=yaml.FullLoader)
