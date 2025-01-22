import logging
import re
from typing import Sequence

from ..typedefs import StringKeyDict
from .factory import get_config_builders
from .types import Config


log = logging.getLogger(__name__)

RE_PLACEHOLDER = re.compile(r"%[a-zA-Z_0-9.-]+%")


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


def _get_items_to_replace(config: StringKeyDict) -> StringKeyDict:
    return {k: v for k, v in config.items() if isinstance(v, str) and RE_PLACEHOLDER.match(v)}


def _unescape(input_data):
    """
    Replaces the '%%' with '%'
    The percentage symbol escapes %some_variable% tokens.
    """
    # config = {k: v.replace("%%", "%") for k, v in config.items()}
    if isinstance(input_data, str):
        return input_data.replace("%%", "%")
    elif isinstance(input_data, list):
        return [_unescape(item) for item in input_data]
    elif isinstance(input_data, dict):
        return {key: _unescape(value) for key, value in input_data.items()}
    else:
        return input_data


def _unflatten_dict(data: StringKeyDict):
    """
    Unflattens a dictionary:
    {"a.b.c": "val"} -> {"a": {"b": {"c": "val"}}}
    """
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


def _interpolate(config: StringKeyDict) -> None:
    are_replacements_left = True
    while are_replacements_left:
        nr_replacements_before = len(_get_items_to_replace(config))
        replacements = {f"%{k}%": v for k, v in config.items() if isinstance(v, str) and not RE_PLACEHOLDER.match(v)}
        for cfg_key, cfg_val in config.items():
            for replacement_key in replacements.keys():
                if replacement_key in cfg_val:
                    config[cfg_key] = cfg_val.replace(replacement_key, replacements[replacement_key])

        replacements_after = _get_items_to_replace(config)
        nr_replacements_after = len(replacements_after)
        if nr_replacements_after > 0 and nr_replacements_after >= nr_replacements_before:
            # No placeholders replaced, but there are still any
            log.error("Failed to resolve:")
            for k, v in replacements_after.items():
                log.error(f"{k} = {v}")
            raise Exception("Cannot resolve placeholders in configuration")
        are_replacements_left = nr_replacements_after > 0


# Credits: https://stackoverflow.com/a/7205107
def _merge(a: dict, b: dict, path=[]):
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                _merge(a[key], b[key], path + [str(key)])
            else:
                a[key] = b[key]

        else:
            a[key] = b[key]
    return a


def compile_config(kwargs: StringKeyDict | Sequence[str] | None = None) -> Config:
    kwargs = _kwargs_to_dict(kwargs)

    cfg: StringKeyDict = {}
    for build in get_config_builders():
        build(cfg)

    cfg = _merge(cfg, kwargs)
    _interpolate(cfg)

    return Config.model_validate(_unflatten_dict(cfg))
