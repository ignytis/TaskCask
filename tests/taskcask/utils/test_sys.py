import unittest

from taskcask.utils import sys


class TestArgsToKwargs(unittest.TestCase):
    def test_args_and_kwargs(self):
        # Test with both args and kwargs
        args = ["foo", "bar=baz", "hello=world", "test"]
        expected_args = ["foo", "test"]
        expected_kwargs = {"bar": "baz", "hello": "world"}
        self.assertEqual(sys.args_to_args_and_kwargs(args), (expected_args, expected_kwargs))

    def test_only_args(self):
        args = ["foo", "bar", "baz"]
        expected_args = ["foo", "bar", "baz"]
        expected_kwargs = {}
        self.assertEqual(sys.args_to_args_and_kwargs(args), (expected_args, expected_kwargs))

    def test_only_kwargs(self):
        args = ["key1=value1", "key2=value2"]
        expected_args = []
        expected_kwargs = {"key1": "value1", "key2": "value2"}
        self.assertEqual(sys.args_to_args_and_kwargs(args), (expected_args, expected_kwargs))

    def test_empty_list(self):
        args = []
        expected_args = []
        expected_kwargs = {}
        self.assertEqual(sys.args_to_args_and_kwargs(args), (expected_args, expected_kwargs))

    def test_edge_case_equal_sign(self):
        args = ["=", "foo=bar", "test=", "=test"]
        expected_args = ["=", "=test"]
        expected_kwargs = {"foo": "bar", "test": ""}
        self.assertEqual(sys.args_to_args_and_kwargs(args), (expected_args, expected_kwargs))
