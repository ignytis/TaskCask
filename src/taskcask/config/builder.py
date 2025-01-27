from abc import ABC

from ..typedefs import ConfigDict


class BaseConfigBuilder(ABC):
    def build(self, config: ConfigDict) -> ConfigDict:
        raise NotImplementedError()
