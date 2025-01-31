from pydantic import BaseModel


class BaseTaskTemplate(BaseModel):
    kind: str
    print_output: bool | None = None
