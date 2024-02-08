import unittest

from eml.resources import EMLSoftware
from test_xml.test_xml import TestXML


class TestEMLSoftware(TestXML):
    def test_not_implemented(self):
        self.assertRaises(NotImplementedError, EMLSoftware)


if __name__ == '__main__':
    unittest.main()
