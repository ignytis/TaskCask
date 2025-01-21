from pydantic import BaseModel


# TODO: remove??
class TaskTemplateLoaderDirYamlConfig(BaseModel):
    path: str = ""
