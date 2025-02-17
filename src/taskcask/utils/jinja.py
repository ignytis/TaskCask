import jinja2
import os.path


def jinja_render_from_file(path: str, ctx: dict):
    """
    Renders a file from path.
    Uses FileSystemLoader to lookup Jinja template paths relatively to the specified one.
    """
    dir = os.path.dirname(path)
    filename = os.path.basename(path)
    jinja_env = jinja2.Environment(undefined=jinja2.StrictUndefined, loader=jinja2.FileSystemLoader(dir))
    tpl = jinja_env.get_template(filename)
    return tpl.render(ctx)
