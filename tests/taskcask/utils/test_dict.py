from unittest import TestCase

from taskcask.utils.dict import dict_deep_merge, dict_unflatten


class DictMergeTest(TestCase):
    def test_int_list(self) -> None:
        dict1 = {"a": 1, "b": {"x": 10, "y": 20}}
        dict2 = {"b": {"y": 30, "z": 40}, "c": 3}
        dict3 = {"d": 4, "b": {"y": 50}}

        self.assertDictEqual(
            {"a": 1, "b": {"x": 10, "y": 50, "z": 40}, "c": 3, "d": 4},
            dict_deep_merge(dict1, dict2, dict3))

    def test_int_list_str_vs_dict(self) -> None:
        dict1 = {"a": 1, "b": "abc"}
        dict2 = {"b": {"y": 30, "z": 40}, "c": 3}
        dict3 = {"d": 4, "b": {"y": 50}}

        self.assertDictEqual(
            {"a": 1, "b": {"y": 50, "z": 40}, "c": 3, "d": 4},
            dict_deep_merge(dict1, dict2, dict3))

    def test_int_list_dict_vs_str(self) -> None:
        dict1 = {"a": 1, "b": {"x": 10, "y": 20}}
        dict2 = {"b": {"y": 30, "z": 40}, "c": 3}
        dict3 = {"d": 4, "b": "abc"}

        self.assertDictEqual(
            {"a": 1, "b": "abc", "c": 3, "d": 4},
            dict_deep_merge(dict1, dict2, dict3))


class DictUnflattenTest(TestCase):
    def test_unflatten(self) -> None:
        self.assertDictEqual(
            {"a": "one", "b": {"c": {"d": "two", "e": False}, "f": 4}},
            dict_unflatten({"a": "one", "b.c.d": "two", "b.c.e": False, "b.f": 4}),
        )

    def test_unflatten_invalid_assign_value_to_non_dictionary(self) -> None:
        with self.assertRaisesRegex(
                ValueError,
                "Attempting to assign a value 'two' with key 'b' to  non-dictionary 'one'"):
            dict_unflatten({"a": "one", "a.b": "two"})
