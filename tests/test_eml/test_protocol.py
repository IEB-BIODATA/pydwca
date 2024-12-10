import unittest

from lxml import etree as et

from eml.resources import EMLProtocol
from test_xml.test_xml import TestXML


class TestEMLProtocol(TestXML):
    DEFAULT_TAGS = {
        "scope": "document"
    }

    def test_parse_referencing(self):
        text_xml = """
<protocol>
    <references>protocol-id</references>
</protocol>
        """
        protocol = EMLProtocol.from_string(text_xml)
        self.assertTrue(protocol.referencing, "Referencing parse incorrectly")
        self.assertEqual("protocol-id", protocol.id, "Id parse incorrectly")
        self.assertEqualTree(et.fromstring(text_xml), protocol.to_element(), "Error on to element")


if __name__ == '__main__':
    unittest.main()
