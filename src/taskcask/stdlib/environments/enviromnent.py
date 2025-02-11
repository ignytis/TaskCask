from enum import Enum
from typing import Literal

from ...environments.environment import BaseEnvironment
from ...typedefs import EnvVars, BaseModel


class LocalEnvironment(BaseEnvironment):
    """
    Local machine
    """
    kind: Literal["local"] = "local"
    env: EnvVars
    """Environment variables"""


class SshEnvironment(BaseEnvironment):
    """
    Remote server (SSH connection)
    """
    kind: Literal["ssh"] = "ssh"
    env: EnvVars
    host: str
    port: str = "22"
    user: str
    """Environment variables"""


class DockerEnvironmentVolumeMountMode(Enum):
    ro = "ro"
    """Read-only mode"""
    rw = "rw"
    """Read and Write mode"""


class DockerEnvironmentVolume(BaseModel):
    host_path: str
    """path the host system"""
    container_path: str
    """path inside container"""
    mode: DockerEnvironmentVolumeMountMode = DockerEnvironmentVolumeMountMode.ro


class DockerEnvironment(BaseEnvironment):
    """
    Remote server (SSH connection)
    """
    kind: Literal["docker"] = "docker"
    env: EnvVars
    """Environment variables"""
    image: str
    """Image to use"""
    volumes: list[DockerEnvironmentVolume] = []
    """Volumes to mount"""
