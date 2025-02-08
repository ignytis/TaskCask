from unittest import TestCase
from unittest.mock import patch, mock_open

from taskcask.config.compiler import compile_config

FILE_CONFIG_CONTENTS = """\
{% set name = "John" %}
parameters:
  name: {{ name }}
  greeting: "Hello, {{ name }}!"
"""


@patch("pathlib.Path.cwd", return_value="/test/cwd")
@patch("pathlib.Path.home", return_value="/test/home")
@patch("builtins.open", new_callable=mock_open, read_data=FILE_CONFIG_CONTENTS)
@patch("os.path.isfile", return_value=True)
@patch("os.path.getmtime", return_value=123)
class CompilerTest(TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.maxDiff = None

    def test_compile_simple(self, _a, _b, _c, _d, _e) -> None:
        self.assertDictEqual({
            "io": {
                "print_result": True,
            },
            "sys": {
                "cwd": "/test/cwd",
                "home": "/test/home",
            },
            "environments": {},
            "parameters": {
                "name": "John",
                "greeting": "Hello, John!",
            },
            "task_template_loaders": {},
        }, compile_config().model_dump())
