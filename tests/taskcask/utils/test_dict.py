from unittest import TestCase

from taskcask.utils.dict import dict_deep_merge


class DictMergeTest(TestCase):
    def test_int_list(self) -> None:
        dict1 = {"a": 1, "b": {"x": 10, "y": 20}}
        dict2 = {"b": {"y": 30, "z": 40}, "c": 3}
        dict3 = {"d": 4, "b": {"y": 50}}

        self.assertDictEqual(
            {"a": 1, "b": {"x": 10, "y": 50, "z": 40}, "c": 3, "d": 4},
            dict_deep_merge(dict1, dict2, dict3))
