from importlib.metadata import entry_points


_plugins_loaded: bool = False


def load_plugins() -> None:
    """
    Loads plugins globally. This function ensures that plugins are initialized only once.
    """
    global _plugins_loaded
    for ep in entry_points(group="taskcask.autoloaders"):
        ep.load()
    _plugins_loaded = True
