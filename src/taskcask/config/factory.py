from importlib.metadata import entry_points
from typing import Callable, Generator

from .types import Config


def get_config_builders() -> Generator[Callable[[Config], None], None, None]:
    for entry_point in entry_points(group="taskcask.config.builders"):
        yield entry_point.load()
