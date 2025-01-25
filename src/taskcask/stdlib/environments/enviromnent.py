from typing import Literal

from ...environments.environment import BaseEnvironment
from ...typedefs import StringKvDict


class LocalEnvironment(BaseEnvironment):
    kind: Literal["local"] = "local"
    env: StringKvDict
    """Environment variables"""
