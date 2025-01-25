from unittest import TestCase
from unittest.mock import patch, mock_open


CONFIG_CONTENTS = b"""\
[task_template_loaders.dir_toml]
path = "%sys.home%/my_app/my_templates"
"""


class BuilderTest(TestCase):
    @patch("pathlib.Path.cwd")
    @patch("pathlib.Path.home")
    @patch("builtins.open", new_callable=mock_open, read_data=CONFIG_CONTENTS)
    def test_builder(self, _mock_file, home, cwd):
        home.return_value = "/home/mock_user"
        cwd.return_value = "/var/mock_cwd"

        from taskcask.stdlib.config import builder

        cfg = {}
        builder.build(cfg)

        self.assertDictEqual(cfg, {
            "sys.cwd": "/var/mock_cwd",
            "sys.home": "/home/mock_user",
            "task_template_loaders.dir_toml.path": "%sys.home%/my_app/my_templates"
        })
