from importlib.metadata import entry_points


def load_plugins() -> None:
    for ep in entry_points(group="taskcask.autoloaders"):
        ep.load()
