from abc import ABC

from ..config.types import Config


class BaseConfigBuilder(ABC):
    def __init__(self, kwargs: dict):
        self.kwargs = {**kwargs}

    def build(self, config: Config) -> Config:
        raise NotImplementedError()
