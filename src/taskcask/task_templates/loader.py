from pathlib import Path
from typing import Generator

from configtpl.config_builder import ConfigBuilder

from ..config.types import Config
from taskcask_common.typedefs import TaskTemplateDefinition


def get_task_template_definitions(config: Config) -> Generator[dict[str, TaskTemplateDefinition], None, None]:
    """
    Generates the dictionaries of task template definitions (which are dicrionaties of task template attributes).
    Keys are task template identifiers.
    """
    builder = ConfigBuilder()
    for loader_cfg_path in config.task_templates.lookup_dirs:
        for task_def_tpl_path in Path(loader_cfg_path).rglob("*.tcask"):
            yield builder.build_from_files(str(task_def_tpl_path), ctx={"cfg": config})
