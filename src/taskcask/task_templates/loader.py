from pathlib import Path
from typing import Generator

from ..config.types import Config
from ..config.tcask_file_loader import tcask_file_load_with_config
from taskcask_common.typedefs import TaskTemplateDefinition


def get_task_template_definitions(config: Config) -> Generator[dict[str, TaskTemplateDefinition], None, None]:
    """
    Generates the dictionaries of task template definitions (which are dicrionaties of task template attributes).
    Keys are task template identifiers.
    """
    for loader_cfg_path in config.task_templates.lookup_dirs:
        for task_def_tpl_path in Path(loader_cfg_path).rglob("*.tcask"):
            yield tcask_file_load_with_config(task_def_tpl_path, config)
