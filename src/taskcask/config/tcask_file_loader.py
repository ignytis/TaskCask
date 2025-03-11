import yaml

from .types import Config
from ..utils.jinja import jinja_render_from_file

from taskcask_common.typedefs import StringKeyDict


def tcask_file_load_with_config(path: str, config: Config) -> StringKeyDict:
    """
    Loads a *.tcask file into dictionary
    """
    return yaml.load(jinja_render_from_file(path, {"cfg": config, "params": config.params}),
                     Loader=yaml.FullLoader)
