import unittest

from eml.citation import EMLCitation
from test_xml.test_xml import TestXML


class TestEMLCitation(TestXML):
    def test_not_implemented(self):
        self.assertRaises(NotImplementedError, EMLCitation)


if __name__ == '__main__':
    unittest.main()
