from unittest.mock import patch


@patch("pathlib.Path.cwd")
@patch("pathlib.Path.home")
def test_builder(home, cwd):
    home.return_value = "/home/mock_user"
    cwd.return_value = "/var/mock_cwd"

    from taskcask.config import types as cfg_types
    from taskcask.stdlib.config import builder

    cfg = cfg_types.Config(
        runtime_params=cfg_types.RuntimeParams(),
    )

    builder.build(cfg)

    assert cfg.task_template_loaders.get("dir_yaml", {}).get("path") == \
        "/var/mock_cwd/examples/task_templates/system_commands.yaml"
