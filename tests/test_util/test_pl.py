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
        self.assertEqual(pl.Int64, type_to_pl(int), "Incorrect type (int) to polars type.")

    def test_float(self):
        self.assertEqual(pl.Float64, type_to_pl(float), "Incorrect type (float) to polars type.")

    def test_bool(self):
        self.assertEqual(pl.Boolean, type_to_pl(bool), "Incorrect type (bool) to polars type.")

    def test_datetime(self):
        self.assertEqual(pl.Datetime, type_to_pl(dt.datetime), "Incorrect type (datatime) to polars type.")

    def test_str(self):
        self.assertEqual(pl.String, type_to_pl(str), "Incorrect type (str) to polars type.")

    def test_list(self):
        self.assertEqual(pl.List(pl.String), type_to_pl(List[str]), "Incorrect type (List[str]) to polars type.")
        self.assertEqual(pl.List(pl.Object), type_to_pl(List[TestType]), "Incorrect type (List[obj]) to polars type.")
        self.assertEqual(pl.List(pl.Object), type_to_pl(List), "Incorrect type (List[obj]) to polars type.")
        self.assertEqual(pl.String, type_to_pl(List[str], lazy=True), "Incorrect type [lazy] (List[str]) to polars type.")

    def test_nested_list(self):
        self.assertEqual(pl.List(pl.List(pl.String)), type_to_pl(List[List[str]]), "Incorrect type (List[List[str]]) to polars type.")
        self.assertEqual(pl.List(pl.List(pl.Object)), type_to_pl(List[List[TestType]]), "Incorrect type (List[List[obj]]) to polars type.")
        self.assertEqual(pl.List(pl.List(pl.List(pl.Int64))), type_to_pl(List[List[List[int]]]),
                         "Incorrect type (List[List[List[int]]]) to polars type.")
        self.assertEqual(pl.String, type_to_pl(List[List[List[int]]], lazy=True),
                         "Incorrect type [lazy] (List[List[List[int]]]) to polars type.")

    def test_obj(self):
        self.assertEqual(pl.Object, type_to_pl(TestType), "Incorrect type (obj) to polars type.")
        self.assertEqual(pl.String, type_to_pl(TestType, lazy=True), "Incorrect type [lazy] (obj) to polars type.")



if __name__ == '__main__':
    unittest.main()
