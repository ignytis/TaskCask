from pydantic import BaseModel


class BaseTaskTemplate(BaseModel):
    kind: str
    print_result: bool | None = None
