import os
import sys
import unittest
from unittest.mock import patch

from dwca.base import DarwinCoreArchive
from test_dwca.test_dwca_common import TestDWCACommon

PATH = os.path.abspath(os.path.dirname(__file__))

orig_import = __import__


def import_mock(name, globals=None, locals=None, fromlist=(), level=0):
    if name == 'pandas':
        raise ImportError(f"No module named '{name}'")
    return orig_import(name, globals, locals, fromlist, level)


class TestDWCANoPandas(TestDWCACommon):
    @patch('builtins.__import__', side_effect=import_mock)
    def test_minimal(self, mock_import):
        super().__test_minimal__()

    @patch('builtins.__import__', side_effect=import_mock)
    def test_attributes(self, mock_import):
        super().__test_attributes__()

    @patch('builtins.__import__', side_effect=import_mock)
    def test_merge(self, mock_import):
        super().__test_merge__()

    @patch('builtins.__import__', side_effect=import_mock)
    def test_set_core(self, mock_import):
        core = self.object.core
        self.assertEqual(163460, len(core), "Wrong number of entries")
        core.__entries__ = core.__entries__[0:100]
        self.assertEqual(100, len(core), "Core has not been shorted to 100 entries")
        self.object.core = core
        self.assertEqual(100, len(self.object.core), "Core has not been shorted on DwC-A object")
        for extension in self.object.extensions:
            self.assertGreaterEqual(100, len(extension), f"Extension {extension.uri} has not been shorted")


if __name__ == '__main__':
    unittest.main()
