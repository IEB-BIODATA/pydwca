import os.path
import sys
import unittest

from dwca.classes import OutsideClass
from test_dwca_classes.test_outside_class_common import TestOutsideCommon

PATH = os.path.abspath(os.path.dirname(__file__))


class TestOutside(TestOutsideCommon):
    def setUp(self) -> None:
        sys.modules['pandas'] = None
        self.outside_xml, self.text = self.read_xml(os.path.join(PATH, os.pardir, "example_data", "meta.xml"))
        return

    def tearDown(self) -> None:
        del sys.modules['pandas']
        return

    def test_parse(self):
        super().__test_parse__()

    def test_none(self):
        super().__test_none__()

    def test_merge(self):
        super().__test_merge__()


if __name__ == '__main__':
    unittest.main()
