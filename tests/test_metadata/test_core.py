import os.path
import unittest

import lxml.etree as et

from dwca.metadata import Core
from test_xml.test_xml import TestXML


class TestCore(TestXML):
    def setUp(self) -> None:
        with open(os.path.join("example_data", "meta.xml"), "r", encoding="utf-8") as file:
            content = file.read()
        base_file = et.fromstring(content)
        self.core_xml = base_file.find("core", namespaces=base_file.nsmap)
        self.text = et.tostring(self.core_xml, pretty_print=True).decode("utf-8")
        return

    def test_parse(self):
        core = Core.from_string(self.text)
        self.assertEqual("taxon.txt", core.__files__, "Files parse incorrectly")
        self.assertEqual(0, core.__id__, "Files parse incorrectly")
        self.assertEqual("UTF-8", core.__encoding__, "Encoding parse incorrectly")
        self.assertEqual("\\r\\n", core.__lines_end__, "Lines end parse incorrectly")
        self.assertEqual("\\t", core.__fields_end__, "Field end parse incorrectly")
        self.assertEqual("", core.__fields_enclosed__, "Field enclosed parse incorrectly")
        self.assertEqual([1], core.__ignore_header__, "Ignore header parse incorrectly")
        self.assertEqual("http://rs.tdwg.org/dwc/terms/Taxon", core.__row_type_url__, "Row type parse incorrectly")
        self.assertEqual(31, len(core.__fields__), "Fields parse incorrectly")
        self.assertEqualTree(self.core_xml, core.to_element(), "Error on element conversion")

    def test_none(self):
        self.assertIsNone(Core.parse(None, {}), "Object parsed from nothing")

    def test_parse_invalid(self):
        self.assertRaises(
            AssertionError,
            Core.from_string,
            '<extension />'
        )


if __name__ == '__main__':
    unittest.main()
