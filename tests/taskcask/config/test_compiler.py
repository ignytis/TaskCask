from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch, mock_open

from taskcask.config.compiler import compile_config, _format_config_value, _format_env_key

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
  load_next_defer:
  - another_config.tcask
"""

FILE_CONFIG_CONTENTS_COMPOSITE_SECOND = """\
task_templates:
  lookup_dirs:
  - /home/{{ params.user_name | lower }}
"""

CONFIG_COMPILED_SIMPLE = {
    "environments": {},
    "io": {
        "print_result": True,
    },
    "params": {
        "user_name": "John",
        "greeting": "Hello, John!",
    },
    "sys": {
        "cwd": "/test/cwd",
        "home": "/test/home",
    },
    "task_templates": {
        "lookup_dirs": []
    },
}

ENV_VARS = [("TASKCASK__PARAMS__ENV_VAR_ONE", "env_var1"),
            ("TASKCASK__PARAMS__ENV_VAR_OVERRIDE", "to_be_overridden")]


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

    @patch("builtins.open", new_callable=mock_open, read_data=FILE_CONFIG_CONTENTS_SIMPLE)
    @patch("os.environ.items", return_value=ENV_VARS)
    def test_compile_simple_override(self, _a, _b, _c, _d, _e, _f) -> None:
        cfg_compiled = deepcopy(CONFIG_COMPILED_SIMPLE)
        cfg_compiled["params"] = {
            **cfg_compiled["params"],
            "some_param": "some_param_val1",
            "env_var_one": "env_var1",
            "env_var_override": "some_param_val2",
        }
        self.assertDictEqual(cfg_compiled, compile_config(["params.some_param=some_param_val1",
                                                           "params.env_var_override=some_param_val2"]).model_dump())

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
            "task_templates": {
                "lookup_dirs": ["/home/john"]
            },
        }, compile_config().model_dump())


class TestConfigFormatting(TestCase):
    def test_format_env_key(self):
        self.assertEqual(_format_env_key("TASKCASK__SOME__MY_VAR"), "some.my_var")
        self.assertEqual(_format_env_key("TASKCASK__ANOTHER_VAR"), "another_var")
        self.assertEqual(_format_env_key("TASKCASK__VAR"), "var")

    def test_format_config_value(self):
        self.assertEqual(_format_config_value("123"), 123)
        self.assertEqual(_format_config_value("-456"), -456)
        self.assertEqual(_format_config_value("3.14"), 3.14)
        self.assertEqual(_format_config_value('"3.14"'), "3.14")
        self.assertEqual(_format_config_value("-2.71"), -2.71)
        self.assertEqual(_format_config_value("true"), True)
        self.assertEqual(_format_config_value("false"), False)
        self.assertEqual(_format_config_value('"false"'), "false")
        self.assertEqual(_format_config_value("SomeText"), "SomeText")
        self.assertEqual(_format_config_value("123abc"), "123abc")
