from typing import Literal

from taskcask_common.environment import BaseEnvironment
from taskcask_common.typedefs import EnvVars


class LocalEnvironment(BaseEnvironment):
    """
    Local machine
    """
    kind: Literal["local"] = "local"
    env: EnvVars
    """Environment variables"""
