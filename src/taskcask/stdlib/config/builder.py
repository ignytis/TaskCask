import logging
from pathlib import Path
import os

from config import config_from_toml, config_from_env, config_from_dict, ConfigurationSet

from ...typedefs import StringKeyDict

PATH_HOME = str(Path.home())


log = logging.getLogger(__name__)


def build(config: StringKeyDict) -> None:
    cfgs = [
        config_from_env(prefix="TASKCASK"),
        config_from_dict({
            "sys": {
                "cwd": str(Path.cwd()),
                "home": PATH_HOME,
            },
        })
    ]
    cfg_path = os.getenv("TASKCASK_CONFIG", f"{PATH_HOME}/.taskcask/config.toml")
    if cfg_path:
        cfgs.insert(1, config_from_toml(data=cfg_path, read_from_file=True))
    cfg_dict: StringKeyDict = ConfigurationSet(*cfgs).as_dict()
    config.update(cfg_dict)
