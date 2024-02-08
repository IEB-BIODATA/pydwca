import unittest

from lxml import etree as et

from eml.resources.distribution import EMLInline
from test_xml.test_xml import TestXML


class TestInline(TestXML):
    def test_parse(self):
        text_xml = """
<inline></inline>
        """
        inline = EMLInline.from_string(text_xml)
        self.assertEqualTree(et.fromstring(text_xml), inline.to_element(), "Error on to element")

    def test_parse_none(self):
        self.assertIsNone(EMLInline.parse(None, {}), "EML Inline from nowhere")


if __name__ == '__main__':
    unittest.main()
