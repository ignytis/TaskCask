from abc import ABC

from ..config.types import Config


class BaseConfigBuilder(ABC):
    def build(self, config: Config) -> Config:
        raise NotImplementedError()
