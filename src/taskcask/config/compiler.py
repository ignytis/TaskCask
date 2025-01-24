import logging
import re
from typing import Sequence

from ..typedefs import StringKeyDict, StringKvDict
from .factory import get_config_builders
from .types import Config


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


class CircularReferenceException(Exception):
    def __init__(self, stack: list[str], *args):
        super().__init__(*args)
        self.stack = stack


def _topological_sort(graph):
    # Dictionary to keep track of visited status: 0 - not visited, 1 - visiting, 2 - visited
    visited = {}
    stack = []

    def dfs(node):
        if visited.get(node) == 1:
            raise CircularReferenceException([node])

        # If node has not been visited before, mark it as visiting
        if visited.get(node) == 0:
            visited[node] = 1  # Mark as visiting
            for neighbor in graph[node]:
                try:
                    dfs(neighbor)
                except CircularReferenceException as e:
                    raise CircularReferenceException([node] + e.stack)
            visited[node] = 2  # Mark as visited
            stack.append(node)

    # Initialize all nodes as not visited
    for node in graph:
        visited[node] = 0

    # Perform DFS for all nodes not yet visited
    for node in graph:
        if visited[node] == 0:
            dfs(node)

    return stack


def _render_value(value: str, replacements: StringKeyDict) -> str:
    """
    Replace placeholders (%abc%) with values.
    Skip the escaped values (%%abc%%)
    """
    # -1 because non-inclusive end()
    idxs: list[int] = [(m.start(), m.end()-1) for m in RE_PLACEHOLDER.finditer(value)]
    # Check occurrences in reverse order: this way updates in string will not affect the
    # previously located indexes
    idxs.reverse()
    for idx_start, idx_end in idxs:
        idx_last_char = len(value) - 1
        char_before = None if idx_start == 0 else value[idx_start-1]
        char_after = None if idx_end == idx_last_char else value[idx_end+1]
        is_escape_before = "%" == char_before
        is_escape_after = "%" == char_after
        # Escape sequence found: unescape
        if is_escape_before and is_escape_after:
            continue

        # No escape sequence found: replace the value
        replacement_key = value[idx_start+1:idx_end]
        if replacement_key not in replacements:
            raise ValueError(f"Key '{replacement_key}' not found")
        replace_with = replacements[replacement_key]
        value = value[:idx_start] + replace_with + value[idx_end+1:]

    return value


def _interpolate(config: StringKeyDict) -> None:
    # Dependency tree: parents depend on children
    dep_kv: StringKvDict = {}
    for parent, v in config.items():
        children = RE_PLACEHOLDER.findall(v)
        dep_kv[parent] = children

    try:
        sorted_cfg_keys = _topological_sort(dep_kv)
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
    cfg = _unescape(cfg)

    return Config.model_validate(_unflatten_dict(cfg))
