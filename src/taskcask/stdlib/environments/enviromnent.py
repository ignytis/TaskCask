from typing import Literal

from ...environments.environment import BaseEnvironment
from ...typedefs import StringKvDict


class LocalEnvironment(BaseEnvironment):
    kind: Literal["local"] = "local"
    env: StringKvDict
    """Environment variables"""


class SshEnvironment(BaseEnvironment):
    kind: Literal["ssh"] = "ssh"
    env: StringKvDict
    host: str
    port: str = "22"
    user: str
    """Environment variables"""
