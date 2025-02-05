import logging
import os
# import re

import jinja2
import yaml

from ...typedefs import StringKeyDict
from ...config.builder import BaseConfigBuilder
from ...config.types import Config
from ...utils.dict import dict_deep_merge


# RE_UNDERSCORE = re.compile(r"_{2,}")


class ConfigBuilder(BaseConfigBuilder):
    """
    Standard config builder.
    Renders the config files as Jinja templates and parses the results as YAML.
    """
    log = logging.getLogger(__name__)

    def build(self, config: Config) -> Config:
        cfg_paths = os.getenv("TASKCASK_CONFIG", os.path.join(config.sys.home, ".taskcask", "config.toml.jinja2")) \
            .split(os.pathsep)
        loaded_cfg_paths = []  # protection against recursion

        while len(cfg_paths) > 0:
            cfg_path = os.path.realpath(cfg_paths.pop(0))
            if cfg_path in loaded_cfg_paths:
                raise Exception(f"Attempting to load the path '{cfg_path}' multiple times")
            loaded_cfg_paths.append(cfg_path)
            cfg_filename = os.path.basename(cfg_path)
            cfg_dir = os.path.dirname(cfg_path)
            cfg_path = None
            jinja_env = jinja2.Environment(undefined=jinja2.StrictUndefined, loader=jinja2.FileSystemLoader(cfg_dir))

            tpl = jinja_env.get_template(cfg_filename)
            cfg_iter: StringKeyDict = yaml.load(tpl.render({"cfg": config}), Loader=yaml.FullLoader)

            config = dict_deep_merge(config.model_dump(), cfg_iter)
            config = Config.model_validate(config)

            # Add next templates to load if any
            taskcask_directives: StringKeyDict | None = cfg_iter.get("_taskcask_directives")
            if taskcask_directives is not None:
                # Consider path to current config
                new_cfg_paths = [os.path.realpath(os.path.join(cfg_dir, p))
                                 for p in taskcask_directives.get("load_next", [])]
                cfg_paths += new_cfg_paths
                del cfg_iter["_taskcask_directives"]

        # # TODO:
        # Also consider CLI/dictionary params
        # cfg_env = {_format_env_key(k): v for k, v in os.environ.items() if k.startswith("TASKCASK__")}

        return config


# def _format_env_key(key: str) -> str:
#     return key.lower().replace(RE_UNDERSCORE, ".")
