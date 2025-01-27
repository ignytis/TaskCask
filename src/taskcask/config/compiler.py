import logging
import re
from typing import Sequence

from .builder import BaseConfigBuilder
from ..typedefs import ConfigDict, StringKeyDict, StringKvDict
from .types import Config
from ..utils.algorithms.sort import sort_topological, CircularReferenceException
from ..utils.dict import dict_deep_merge, dict_unflatten
from ..utils.reflection import get_all_subclasses

log = logging.getLogger(__name__)

RE_PLACEHOLDER = re.compile(r"%([a-zA-Z_0-9._-]+)%")


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


def _render_value(value: str, replacements: StringKeyDict) -> str:
    """
    Replace placeholders (%abc%) with values.
    Skip the escaped values (%%abc%%)
    """
    # -1 because non-inclusive end()
    idxs: list[int] = [m.span() for m in RE_PLACEHOLDER.finditer(value)]
    # Check occurrences in reverse order: this way updates in string will not affect the
    # previously located indexes
    idxs.reverse()
    for idx_start, idx_end_noninclusive in idxs:
        idx_end = idx_end_noninclusive - 1
        idx_last_char = len(value) - 1
        char_before = None if idx_start == 0 else value[idx_start-1]
        char_after = None if idx_end == idx_last_char else value[idx_end+1]
        # Escape sequence found: no action.
        # Unescape will occur on later stage when all references are resolved.
        if "%" == char_before and "%" == char_after:
            continue

        # No escape sequence found: replace the value
        replacement_key = value[idx_start+1:idx_end]
        if replacement_key not in replacements:
            raise ValueError(f"Key '{replacement_key}' not found")
        replace_with = replacements[replacement_key]
        value = value[:idx_start] + replace_with + value[idx_end+1:]

    return value


def _interpolate(config: ConfigDict) -> None:
    # Dependency tree: parents depend on children
    dep_kv: StringKvDict = {}
    for parent, v in config.items():
        if not isinstance(v, str):
            continue
        children = RE_PLACEHOLDER.findall(v)
        dep_kv[parent] = children

    try:
        sorted_cfg_keys = sort_topological(dep_kv)
    except CircularReferenceException as e:
        stack = " -> ".join(e.stack)
        raise ValueError(f"A circular reference detected: {stack}")
    for cfg_key in sorted_cfg_keys:
        children_keys = dep_kv[cfg_key]
        missing_keys = children_keys - config.keys()
        if len(missing_keys) > 0:
            raise ValueError(f'Keys not found in config: {", ".join(missing_keys)}')
        # Key: placeholder key, value: value to replace with
        children_replacements = {child_key: config[child_key] for child_key in children_keys}
        config[cfg_key] = _render_value(config[cfg_key], children_replacements)


def compile_config(kwargs: StringKeyDict | Sequence[str] | None = None) -> Config:
    kwargs = _kwargs_to_dict(kwargs)

    cfg: ConfigDict = {}
    for ConfigBuilder in get_all_subclasses(BaseConfigBuilder):
        builder: BaseConfigBuilder = ConfigBuilder()
        cfg = builder.build(cfg)

    cfg = dict_deep_merge(cfg, kwargs)
    _interpolate(cfg)
    cfg = _unescape(cfg)

    return Config.model_validate(dict_unflatten(cfg))
