import unittest

from lxml import etree as et

from eml.resources import EMLCitation
from test_xml.test_xml import TestXML


class TestEMLCitation(TestXML):
    DEFAULT_TAGS = {
        "scope": "document"
    }

    def test_parse_referencing(self):
        text_xml = """
<citation>
    <references>cite-id</references>
</citation>
        """
        citation = EMLCitation.from_string(text_xml)
        self.assertTrue(citation.referencing, "Referencing parse incorrectly")
        self.assertEqual("cite-id", citation.id, "Id parse incorrectly")
        self.assertEqualTree(et.fromstring(text_xml), citation.to_element(), "Error on to element")


if __name__ == '__main__':
    unittest.main()
