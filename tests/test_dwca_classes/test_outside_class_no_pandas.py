import os.path
import sys
import unittest
from unittest.mock import patch

from test_dwca_classes.test_outside_class_common import TestOutsideCommon

PATH = os.path.abspath(os.path.dirname(__file__))

orig_import = __import__


def import_mock(name, globals=None, locals=None, fromlist=(), level=0):
    if name == 'pandas':
        raise ImportError(f"No module named '{name}'")
    return orig_import(name, globals, locals, fromlist, level)


class TestOutsideNoPandas(TestOutsideCommon):
    @patch('builtins.__import__', side_effect=import_mock)
    def test_parse(self, mock_import):
        super().__test_parse__()

    @patch('builtins.__import__', side_effect=import_mock)
    def test_none(self, mock_import):
        super().__test_none__()

    @patch('builtins.__import__', side_effect=import_mock)
    def test_merge(self, mock_import):
        super().__test_merge__()

    @patch('builtins.__import__', side_effect=import_mock)
    def test_set_primary_key(self, mock_import):
        self.__test_set_primary_key__()

    @patch('builtins.__import__', side_effect=import_mock)
    def test_sql_table(self, mock_import):
        self.__test_sql_table__()

    @patch('builtins.__import__', side_effect=import_mock)
    def test_insert(self, mock_import):
        self.__test_insert__()


if __name__ == '__main__':
    unittest.main()
