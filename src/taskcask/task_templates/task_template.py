from pydantic import BaseModel


class BaseTaskTemplate(BaseModel):
    kind: str
