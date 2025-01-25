from pydantic import BaseModel


class BaseEnvironment(BaseModel):
    kind: str
