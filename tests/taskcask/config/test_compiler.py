from unittest import TestCase
from unittest.mock import patch, mock_open

from taskcask.config.compiler import compile_config

FILE_CONFIG_CONTENTS_SIMPLE = """\
{% set name = "John" %}
params:
  user_name: {{ name }}
  greeting: "Hello, {{ name }}!"
"""

FILE_CONFIG_CONTENTS_COMPOSITE_FIRST = """\
{% set name = "John" %}
params:
  user_name: {{ name }}
  greeting: "Hello, {{ name }}!"

"@taskcask":
  load_next:
  - another_config.yaml.jinja2
"""

FILE_CONFIG_CONTENTS_COMPOSITE_SECOND = """\
task_template_loaders:
  sample_loader:
    path: /home/{{ params.user_name | lower }}
"""

CONFIG_COMPILED_SIMPLE = {
    "io": {
        "print_result": True,
    },
    "sys": {
        "cwd": "/test/cwd",
        "home": "/test/home",
    },
    "environments": {},
    "params": {
        "user_name": "John",
        "greeting": "Hello, John!",
    },
    "task_template_loaders": {},
}


@patch("pathlib.Path.cwd", return_value="/test/cwd")
@patch("pathlib.Path.home", return_value="/test/home")
@patch("os.path.isfile", return_value=True)
@patch("os.path.getmtime", return_value=123)
class CompilerTest(TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.maxDiff = None

    @patch("builtins.open", new_callable=mock_open, read_data=FILE_CONFIG_CONTENTS_SIMPLE)
    def test_compile_simple(self, _a, _b, _c, _d, _e) -> None:
        self.assertDictEqual(CONFIG_COMPILED_SIMPLE, compile_config().model_dump())

    @patch("builtins.open", new_callable=mock_open, read_data=FILE_CONFIG_CONTENTS_COMPOSITE_FIRST)
    def test_compile_composite(self, mock_file, _b, _c, _d, _e) -> None:
        handlers = (mock_file.return_value, mock_open(read_data=FILE_CONFIG_CONTENTS_COMPOSITE_SECOND).return_value)
        mock_file.side_effect = handlers

        self.assertDictEqual({
            "io": {
                "print_result": True,
            },
            "sys": {
                "cwd": "/test/cwd",
                "home": "/test/home",
            },
            "environments": {},
            "params": {
                "user_name": "John",
                "greeting": "Hello, John!",
            },
            "task_template_loaders": {
               "sample_loader": {
                  "path": "/home/john"
               }
            },
        }, compile_config().model_dump())
