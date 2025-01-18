from pydantic import BaseModel

from ..typedefs import StringKvDict


class RuntimeParams(BaseModel):
    args: list[str]
    kwargs: StringKvDict

    @staticmethod
    def from_kwargs(kwargs) -> "RuntimeParams":
        result = RuntimeParams(
            args=[],
            kwargs={},
        )

        for arg in kwargs.get("args", ()):
            arg: str = arg
            pos = arg.find("=")
            if -1 == pos:
                result.args.append(arg)
            else:
                result.kwargs[arg[:pos]] = arg[pos+1:]

        return result


class Config(BaseModel):
    runtime_params: RuntimeParams
    task_template_loaders: dict = {}  # task loader configuration
