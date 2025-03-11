from enum import Enum
from typing import Literal

from taskcask_common.environment import BaseEnvironment
from taskcask_common.typedefs import EnvVars, BaseModel


class LocalEnvironment(BaseEnvironment):
    """
    Local machine
    """
    kind: Literal["local"] = "local"
    env: EnvVars
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
    Docker container
    """
    kind: Literal["docker"] = "docker"
    env: EnvVars
    """Environment variables"""
    image: str
    """Image to use"""
    volumes: list[DockerEnvironmentVolume] = []
    """Volumes to mount"""
