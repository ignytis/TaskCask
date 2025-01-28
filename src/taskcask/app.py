from .autoloader import load_plugins
from .config.compiler import compile_config
from .config.types import Config


def app_get_config(params: list[str] | None = None) -> Config:
    if params is None:
        params = []

    load_plugins()
    return compile_config(params)
