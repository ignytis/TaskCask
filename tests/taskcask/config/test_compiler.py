from unittest import TestCase
from unittest.mock import patch


def _mock_build(val: dict):
    val.update({
        "misc.val_from_builder": "builder_value",
        "misc.val_from_builder_override": "override_me",
        "sys.cwd": "/path/one",
        "sys.home": "/path/two",
        "task_template_loaders.sample_loader.loader_param": "hello",
    })


with patch("taskcask.config.factory.get_config_builders") as get_config_builders:
    from taskcask.config import compiler
    get_config_builders.return_value = [_mock_build]


class CompilerTest(TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.maxDiff = None

    def test_builder_simple(self):
        """
        A simple override and interpolation
        """
        cfg = compiler.compile_config({
            "misc.sample_key": "sample_value",
            "misc.val_from_builder_override": "overridden",
        })

        self.assertDictEqual(cfg.model_dump(), {
            "misc": {
                "sample_key": "sample_value",
                "val_from_builder": "builder_value",
                "val_from_builder_override": "overridden",
            },
            "sys": {
                "cwd": "/path/one",
                "home": "/path/two",
            },
            "task_template_loaders": {
                "sample_loader": {
                    "loader_param": "hello"
                }
            },
        })

    def test_recusive_valid(self):
        """
        A recursive interpolation
        """
        cfg = compiler.compile_config({
            "misc.sample_key": "sample_value",
            "misc.recursion_level_1": "abc",
            "misc.recursion_level_3": "Level 2: %task_template_loaders.sample_loader.recursion_level_2%",
            "task_template_loaders.sample_loader.recursion_level_2": "Level 1: %misc.recursion_level_1%",
        })

        self.assertDictEqual(cfg.model_dump(), {
            "misc": {
                "sample_key": "sample_value",
                "val_from_builder": "builder_value",
                "val_from_builder_override": "override_me",
                "recursion_level_1": "abc",
                "recursion_level_3": "Level 2: Level 1: abc",
            },
            "sys": {
                "cwd": "/path/one",
                "home": "/path/two",
            },
            "task_template_loaders": {
                "sample_loader": {
                    "loader_param": "hello",
                    "recursion_level_2": "Level 1: abc",
                }
            },
        })

    def test_recusive_invalid_circular(self):
        """
        A recursive interpolation with circilar reference
        """
        with self.assertRaisesRegex(ValueError, "A circular reference to 'misc.recursion_level_1' detected"):
            compiler.compile_config({
                "misc.sample_key": "sample_value",
                "misc.recursion_level_1": "abc %misc.recursion_level_3%",
                "misc.recursion_level_3": "Level 2: %task_template_loaders.sample_loader.recursion_level_2%",
                "task_template_loaders.sample_loader.recursion_level_2": "Level 1: %misc.recursion_level_1%",
            })

    def test_simple_val_not_found(self):
        """
        A missing value
        """
        with self.assertRaisesRegex(ValueError, "Key 'sample_missing_value' not found in config"):
            compiler.compile_config({
                "misc.sample_key": "sample_value",
                "misc.sample_key_2": "test %sample_missing_value%",
            })
