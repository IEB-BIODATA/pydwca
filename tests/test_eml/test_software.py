import unittest

from lxml import etree as et

from eml.resources import EMLSoftware
from test_xml.test_xml import TestXML


class TestEMLSoftware(TestXML):
    DEFAULT_TAGS = {
        "scope": "document"
    }

    def test_parse_referencing(self):
        text_xml = """
<software>
    <references>software-id</references>
</software>
        """
        software = EMLSoftware.from_string(text_xml)
        self.assertTrue(software.referencing, "Referencing parse incorrectly")
        self.assertEqual("software-id", software.id, "Id parse incorrectly")
        self.assertEqualTree(et.fromstring(text_xml), software.to_element(), "Error on to element")


if __name__ == '__main__':
    unittest.main()
