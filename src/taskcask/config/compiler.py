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


def topological_sort(graph):
    # Dictionary to keep track of visited status: 0 - not visited, 1 - visiting, 2 - visited
    visited = {}
    stack = []

    def dfs(node):
        if visited.get(node) == 1:
            raise ValueError(f"A circular reference to '{node}' detected")

        # If node has not been visited before, mark it as visiting
        if visited.get(node) == 0:
            visited[node] = 1  # Mark as visiting
            for neighbor in graph[node]:
                dfs(neighbor)
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


def _interpolate(config: StringKeyDict) -> None:
    # Dependency tree: parents depend on children
    dep_kv: StringKvDict = {}
    for parent, v in config.items():
        children = RE_PLACEHOLDER.findall(v)
        dep_kv[parent] = children

    sorted_cfg_keys = topological_sort(dep_kv)
    for cfg_key in sorted_cfg_keys:
        children_keys = dep_kv[cfg_key]
        for child_key in children_keys:
            if child_key not in config:
                raise ValueError(f"Key '{child_key}' not found in config")
            if not isinstance(config[child_key], str):
                continue
            config[cfg_key] = config[cfg_key].replace(f"%{child_key}%", config[child_key])


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
