from unittest import TestCase
from unittest.mock import patch, MagicMock


with patch("taskcask.utils.reflection.get_all_subclasses") as get_config_builders:
    mock_builder = MagicMock()
    mock_builder.build.return_value = {
        "misc.val_from_builder": "builder_value",
        "misc.val_from_builder_override": "override_me",
        "sys.cwd": "/path/one",
        "sys.home": "/path/two",
        "task_template_loaders.sample_loader.loader_param": "hello",
    }

    mock_builder_class = MagicMock()
    mock_builder_class.return_value = mock_builder
    get_config_builders.return_value = [mock_builder_class]

    from taskcask.config import compiler


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
            "misc.val_interpolate": "test %misc.val_from_builder_override%",
        })

        self.assertDictEqual({
            "environments": {},
            "misc": {
                "sample_key": "sample_value",
                "val_from_builder": "builder_value",
                "val_from_builder_override": "overridden",
                "val_interpolate": "test overridden",
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
        }, cfg.model_dump())

    def test_simple_error_val_not_found(self):
        """
        A missing value
        """
        with self.assertRaisesRegex(ValueError, "Keys not found in config: sample_missing_value"):
            compiler.compile_config({
                "misc.sample_key": "sample_value",
                "misc.sample_key_2": r"test %sample_missing_value%",
            })

    def test_builder_escaped_val(self):
        """
        Escaped percentage charactef
        """
        cfg = compiler.compile_config({
            "misc.sample_key": "sample_value",
            "misc.val_from_builder_override": "overridden",
            "misc.val_do_not_interpolate": r"test %%misc.val_from_builder_override%%",
        })

        self.assertDictEqual({
            "environments": {},
            "misc": {
                "sample_key": "sample_value",
                "val_from_builder": "builder_value",
                "val_from_builder_override": "overridden",
                "val_do_not_interpolate": "test %misc.val_from_builder_override%",
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
        }, cfg.model_dump())

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

        self.assertDictEqual({
            "environments": {},
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
        }, cfg.model_dump())

    def test_recusive_error_circular_reference(self):
        """
        A recursive interpolation with circilar reference
        """
        with self.assertRaisesRegex(
                ValueError,
                "A circular reference detected: misc.recursion_level_1 -> misc.recursion_level_3 -> "
                "task_template_loaders.sample_loader.recursion_level_2 -> misc.recursion_level_1"):
            compiler.compile_config({
                "misc.sample_key": "sample_value",
                "misc.recursion_level_1": "abc %misc.recursion_level_3%",
                "misc.recursion_level_3": "Level 2: %task_template_loaders.sample_loader.recursion_level_2%",
                "task_template_loaders.sample_loader.recursion_level_2": "Level 1: %misc.recursion_level_1%",
            })
