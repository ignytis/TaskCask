import logging
from pathlib import Path
import os
import re

from config import config_from_toml, config_from_env, config_from_dict, ConfigurationSet

from ...config.types import Config
from ...typedefs import StringKeyDict, ConfigDict

RE_PLACEHOLDER = re.compile(r"%[a-zA-Z_0-9.-]+%")
PATH_HOME = str(Path.home())


log = logging.getLogger(__name__)


def _get_items_to_replace(cfg_dict: StringKeyDict) -> StringKeyDict:
    return {k: v for k, v in cfg_dict.items() if isinstance(v, str) and RE_PLACEHOLDER.match(v)}


def _unescape(input_data):
    """
    Replaces the '%%' with '%'
    The percentage symbol escapes %some_variable% tokens.
    """
    # cfg_dict = {k: v.replace("%%", "%") for k, v in cfg_dict.items()}
    if isinstance(input_data, str):
        return input_data.replace("%%", "%")
    elif isinstance(input_data, list):
        return [_unescape(item) for item in input_data]
    elif isinstance(input_data, dict):
        return {key: _unescape(value) for key, value in input_data.items()}
    else:
        return input_data


def _unflatten_dict(data: StringKeyDict):
    unflattened_dict = {}
    for key, value in data.items():
        sub_keys = key.split(".")
        current_dict = unflattened_dict
        for sub_key in sub_keys[:-1]:
            if sub_key not in current_dict:
                current_dict[sub_key] = {}
            current_dict = current_dict[sub_key]
        current_dict[sub_keys[-1]] = value
    return unflattened_dict


def build(src_cfg: Config) -> None:
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
    cfg_dict = _unescape(cfg_dict)

    # Interpolation.
    # Replaces values of kind %abc% with corresponding values
    # TODO: perhaps the interpolation logic should follow builders.
    #   in this case variables from other builders will be interpolated too
    are_replacements_left = True
    while are_replacements_left:
        nr_replacements_before = len(_get_items_to_replace(cfg_dict))
        replacements = {f"%{k}%": v for k, v in cfg_dict.items() if isinstance(v, str) and not RE_PLACEHOLDER.match(v)}
        for cfg_key, cfg_val in cfg_dict.items():
            for replacement_key in replacements.keys():
                if replacement_key in cfg_val:
                    cfg_dict[cfg_key] = cfg_val.replace(replacement_key, replacements[replacement_key])

        replacements_after = _get_items_to_replace(cfg_dict)
        nr_replacements_after = len(replacements_after)
        if nr_replacements_after > 0 and nr_replacements_after >= nr_replacements_before:
            # No placeholders replaced, but there are still any
            log.error("Failed to resolve:")
            for k, v in replacements_after.items():
                log.error(f"{k} = {v}")
            raise Exception("Cannot resolve placeholders in configuration")
        are_replacements_left = nr_replacements_after > 0

    cfg_dict = _unflatten_dict(cfg_dict)
    src_cfg.task_template_loaders.update(cfg_dict.get("task_template_loaders", {}))

    return cfg_dict
