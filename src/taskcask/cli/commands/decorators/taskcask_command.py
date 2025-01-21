from typing import Callable

from ....config import types
from ....config.factory import get_config_builders


def taskcask_command(orig_fn) -> Callable[..., types.Config]:
    """
    Adds config as a command argument.
    NB: This decorator must FOLLOW Click decorators
    """

    def wrap_fn(**kwargs) -> types.Config:
        cfg = types.Config(
            runtime_params=types.RuntimeParams.from_kwargs(kwargs),
        )

        for build in get_config_builders():
            build(cfg)

        return orig_fn(config=cfg, **kwargs)

    return wrap_fn
