from unittest import TestCase
from unittest.mock import patch


def _mock_build(val: dict):
    val.update({
        "misc.builder_key": "builder_value",
        "misc.attr_to_override": "override_me",
        "task_template_loaders.sample_loader.loader_param": "testing %misc.builder_key%",
    })


class CompilerTest(TestCase):
    @patch("taskcask.config.factory.get_config_builders")
    def test_builder(self, get_config_builders):
        get_config_builders.return_value = [_mock_build]

        from taskcask.config import compiler

        cfg = compiler.compile_config({
            "misc.sample_key": "sample_value",
            "misc.attr_to_override": "overridden",
        })

        self.assertDictEqual(cfg.model_dump(), {
            "misc": {
                "sample_key": "sample_value",
                "builder_key": "builder_value",
                "attr_to_override": "overridden",
            },
            "task_template_loaders": {
                "sample_loader": {
                    "loader_param": "testing builder_value"
                }
            },
        })
