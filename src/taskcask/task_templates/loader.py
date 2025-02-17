import os.path
from pathlib import Path
from typing import Generator

import jinja2
import yaml

from ..config.types import Config
from ..typedefs import TaskTemplateDefinition


def get_task_template_definitions(config: Config) -> Generator[dict[str, TaskTemplateDefinition], None, None]:
    """
    Generates the dictionaries of task template definitions (which are dicrionaties of task template attributes).
    Keys are task template identifiers.
    """
    for loader_cfg_path in config.task_templates.lookup_dirs:
        for task_def_tpl_path in Path(loader_cfg_path).rglob("*.yaml.jinja2"):
            cfg_dir = os.path.dirname(task_def_tpl_path)
            task_def_tpl_filename = os.path.basename(task_def_tpl_path)
            # TODO: make common base environment with task templates
            jinja_env = jinja2.Environment(undefined=jinja2.StrictUndefined, loader=jinja2.FileSystemLoader(cfg_dir))
            tpl = jinja_env.get_template(task_def_tpl_filename)
            yield yaml.load(tpl.render({"cfg": config, "params": config.params}), Loader=yaml.FullLoader)
