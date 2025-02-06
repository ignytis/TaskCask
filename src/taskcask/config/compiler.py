import logging
import re
from typing import Sequence

from .builder import BaseConfigBuilder
from ..typedefs import StringKeyDict
from .types import Config
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


def compile_config(kwargs: StringKeyDict | Sequence[str] | None = None) -> Config:
    kwargs = _kwargs_to_dict(kwargs)

    cfg = Config()
    for ConfigBuilder in get_all_subclasses(BaseConfigBuilder):
        builder: BaseConfigBuilder = ConfigBuilder(kwargs)
        cfg = builder.build(cfg)

    return cfg
