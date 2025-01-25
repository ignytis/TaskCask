from .enviromnent import LocalEnvironment

from typing import Type


def load() -> list[Type]:
    return [LocalEnvironment]
