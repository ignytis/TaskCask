import logging
from pathlib import Path
import os

from config import config_from_toml, config_from_env, config_from_dict, ConfigurationSet

from ...typedefs import StringKeyDict, ConfigDict
from ...config.builder import BaseConfigBuilder


class ConfigBuilder(BaseConfigBuilder):
    log = logging.getLogger(__name__)

    def build(self, config: ConfigDict) -> ConfigDict:
        path_home = str(Path.home())
        cfgs = [
            config_from_env(prefix="TASKCASK"),
            config_from_dict({
                "sys": {
                    "cwd": str(Path.cwd()),
                    "home": path_home,
                },
            })
        ]
        cfg_path = os.getenv("TASKCASK_CONFIG", f"{path_home}/.taskcask/config.toml")
        if cfg_path:
            cfgs.insert(1, config_from_toml(data=cfg_path, read_from_file=True))
        new_cfg: StringKeyDict = ConfigurationSet(*cfgs).as_dict()
        return {**config, **new_cfg}
