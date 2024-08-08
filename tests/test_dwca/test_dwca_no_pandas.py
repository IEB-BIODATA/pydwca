import os
import sys
import unittest

from dwca.base import DarwinCoreArchive
from test_dwca.test_dwca_common import TestDWCACommon
from xml_common.utils import Language

PATH = os.path.abspath(os.path.dirname(__file__))


class TestDWCA(TestDWCACommon):
    def setUp(self) -> None:
        sys.modules['pandas'] = None
        self.object = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "example_archive.zip")
        )
        return

    def tearDown(self) -> None:
        del sys.modules['pandas']
        return

    def test_attributes(self):
        super().__test_attributes__()

    def test_merge(self):
        super().__test_merge__()

    def test_set_core(self):
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
