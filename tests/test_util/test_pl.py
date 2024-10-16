import unittest
from typing import List
from unittest.mock import patch
import datetime as dt
import polars as pl

from xml_common.utils import type_to_pl

orig_import = __import__

def import_mock(name, globals=None, locals=None, fromlist=(), level=0):
    if name == 'polars':
        raise ImportError(f"No module named '{name}'")
    return orig_import(name, globals, locals, fromlist, level)

class TestType:
    pass


class PlFormatTest(unittest.TestCase):
    @patch('builtins.__import__', side_effect=import_mock)
    def test_import_error(self, mock_import):
        self.assertRaisesRegex(ImportError, "polars not installed", type_to_pl, int)

    def test_int(self):
        self.assertEqual(type_to_pl(int), pl.Int64, "Incorrect type (int) to polars type.")

    def test_float(self):
        self.assertEqual(type_to_pl(float), pl.Float64, "Incorrect type (float) to polars type.")

    def test_datetime(self):
        self.assertEqual(type_to_pl(dt.datetime), pl.Datetime, "Incorrect type (datatime) to polars type.")

    def test_str(self):
        self.assertEqual(type_to_pl(str), pl.String, "Incorrect type (str) to polars type.")

    def test_list(self):
        self.assertEqual(type_to_pl(List[str]), pl.List(pl.String), "Incorrect type (List[str]) to polars type.")
        self.assertEqual(type_to_pl(List[TestType]), pl.List(pl.Object), "Incorrect type (List[obj]) to polars type.")
        self.assertEqual(type_to_pl(List), pl.List(pl.Object), "Incorrect type (List[obj]) to polars type.")
        self.assertEqual(type_to_pl(List[str], lazy=True), pl.String, "Incorrect type [lazy] (List[str]) to polars type.")

    def test_nested_list(self):
        self.assertEqual(type_to_pl(List[List[str]]), pl.List(pl.List(pl.String)), "Incorrect type (List[List[str]]) to polars type.")
        self.assertEqual(type_to_pl(List[List[TestType]]), pl.List(pl.List(pl.Object)), "Incorrect type (List[List[obj]]) to polars type.")
        self.assertEqual(type_to_pl(List[List[List[int]]]), pl.List(pl.List(pl.List(pl.Int64))),
                         "Incorrect type (List[List[List[int]]]) to polars type.")
        self.assertEqual(type_to_pl(List[List[List[int]]], lazy=True), pl.String,
                         "Incorrect type [lazy] (List[List[List[int]]]) to polars type.")

    def test_obj(self):
        self.assertEqual(type_to_pl(TestType), pl.Object, "Incorrect type (obj) to polars type.")
        self.assertEqual(type_to_pl(TestType, lazy=True), pl.String, "Incorrect type [lazy] (obj) to polars type.")



if __name__ == '__main__':
    unittest.main()
