import os.path
import unittest
from unittest.mock import patch

from dwca import DarwinCoreArchive
from dwca.classes import OutsideClass
from test_dwca_classes.test_outside_class_common import TestOutsideCommon

PATH = os.path.abspath(os.path.dirname(__file__))

orig_import = __import__


def import_mock(name, globals=None, locals=None, fromlist=(), level=0):
    if name == 'polars':
        raise ImportError(f"No module named '{name}'")
    return orig_import(name, globals, locals, fromlist, level)


class TestOutsideNoPolars(TestOutsideCommon):
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
    def test_missing_field(self, mock_import):
        self.assertRaises(
            AssertionError,
            OutsideClass.from_string,
            """
<core>
    <files>
      <location>missing.txt</location>
    </files>
    <id index="0"/>
    <field index="0" term=""/>
    <field index="1" term=""/>
    <field index="3" term=""/>
</core>
            """
        )

    @patch('builtins.__import__', side_effect=import_mock)
    def test_field_twice(self, mock_import):
        self.assertRaises(
            AssertionError,
            OutsideClass.from_string,
            """
<core>
    <files>
      <location>missing.txt</location>
    </files>
    <id index="0"/>
    <field index="0" term=""/>
    <field index="1" term=""/>
    <field index="3" term=""/>
    <field index="2" term=""/>
    <field index="3" term=""/>
    <field index="4" term=""/>
</core>
            """
        )

    @patch('builtins.__import__', side_effect=import_mock)
    def test_parse_invalid(self, mock_import):
        self.assertRaises(
            AssertionError,
            OutsideClass.from_string,
            '<extension />'
        )
        self.assertRaises(
            KeyError,
            OutsideClass.from_string,
            """
<core-id>
    <field index="0" term=""/>
</core-id>
            """
        )

    @patch('builtins.__import__', side_effect=import_mock)
    def parse_read_lazy(self, mock_import):
        self.assertRaises(
            ImportError,
            DarwinCoreArchive.from_file,
            os.path.join(PATH, os.pardir, "example_data", "example_archive.zip"),
            lazy=True
        )

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
