import unittest

from eml.resources import EMLProtocol
from test_xml.test_xml import TestXML


class TestEMLProtocol(TestXML):
    def test_not_implemented(self):
        self.assertRaises(NotImplementedError, EMLProtocol)


if __name__ == '__main__':
    unittest.main()
