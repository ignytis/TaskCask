import logging
import os
import re
from typing import Sequence

from ..config.tcask_file_loader import tcask_file_load_with_config
from .types import Config
from ..utils.dict import dict_deep_merge, dict_unflatten

from taskcask_common.typedefs import StringKeyDict, StringKvDict

log = logging.getLogger(__name__)

CFG_ENV_PREFIX = "TASKCASK__"
RE_UNDERSCORE = re.compile(r"_{2,}")


def compile_config(kwargs: StringKvDict | Sequence[str] | None = None) -> Config:
    """
    Compiles the configuration from *.tcask files
    """
    config = Config()
    cfg_paths = os.getenv("TASKCASK_CONFIG", os.path.join(config.sys.home, ".taskcask", "config.tcask")) \
        .split(os.pathsep)
    loaded_cfg_paths = []  # protection against recursion

    while len(cfg_paths) > 0:
        cfg_path = os.path.realpath(cfg_paths.pop(0))
        if cfg_path in loaded_cfg_paths:
            raise Exception(f"Attempting to load the path '{cfg_path}' multiple times")
        loaded_cfg_paths.append(cfg_path)
        cfg_dir = os.path.dirname(cfg_path)
        cfg_iter: StringKeyDict = tcask_file_load_with_config(cfg_path, config)
        cfg_path = None

        config = dict_deep_merge(config.model_dump(), cfg_iter)
        config = Config.model_validate(config)

        # Add next templates to load if any
        taskcask_directives: StringKeyDict | None = cfg_iter.get("@taskcask")
        if taskcask_directives is not None:
            # Consider path to current config
            new_cfg_paths = [os.path.realpath(os.path.join(cfg_dir, p))
                             for p in taskcask_directives.get("load_next", [])]
            cfg_paths += new_cfg_paths
            del cfg_iter["@taskcask"]

    cfg_env = {_format_env_key(k): v for k, v in os.environ.items() if k.startswith(CFG_ENV_PREFIX)}
    cfg_overrides = {**cfg_env, **_kwargs_to_dict(kwargs)}
    cfg_overrides = {k: _format_config_value(v) for k, v in cfg_overrides.items()}
    cfg_overrides = dict_unflatten(cfg_overrides)
    config = dict_deep_merge(config.model_dump(), cfg_overrides)
    config = Config.model_validate(config)

    return config


def _kwargs_to_dict(kwargs: StringKeyDict | Sequence[str] | None = None) -> StringKeyDict:
    """
    Convert kwargs to dict
    """
    if kwargs is None:
        kwargs = {}
    elif isinstance(kwargs, list) or isinstance(kwargs, Sequence):
        # convert ["param1=val1", "param2=val2"] into dict
        _kwargs = {}
        for a in kwargs:
            i = a.index("=")
            if i < 0:
                continue
            k = a[:i]
            v = a[i+1:]
            _kwargs[k] = v

        kwargs = _kwargs

    return kwargs


def _format_env_key(key: str) -> str:
    """
    Example: TASKCASK__SOME__MY_VAR -> some.my_var
    """
    return RE_UNDERSCORE.sub(".", key.removeprefix(CFG_ENV_PREFIX).lower())


def _format_config_value(orig_value: str) -> str | float | int | bool:
    """
    Replace the string value with more suitable type
    """
    is_quoted = orig_value.startswith('"') and orig_value.endswith('"')
    value = orig_value[1:-1] if is_quoted else orig_value

    # If value is a quoted string e.g. "false" -> return unquoted string,
    # but do NOT convert the type
    if is_quoted:
        return value

    # Try converting to integer
    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
        return int(value)

    # Try converting to float
    try:
        float_value = float(value)
        return float_value
    except ValueError:
        pass

    # Try converting to boolean
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"

    # Keep as string
    return value
