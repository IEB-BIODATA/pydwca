import os.path
import unittest

from lxml import etree as et

from dwca.classes import OutsideClass
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestOutside(TestXML):
    def setUp(self) -> None:
        with open(os.path.join(PATH, os.pardir, "example_data", "meta.xml"), "r", encoding="utf-8") as file:
            content = file.read()
        base_file = et.fromstring(content)
        self.outside_xml = base_file.findall("extension", namespaces=base_file.nsmap)[0]
        self.text = et.tostring(self.outside_xml, pretty_print=True).decode("utf-8")
        return

    def test_parse(self):
        outside = OutsideClass.from_string(self.text)
        self.assertEqual("speciesprofile.txt", outside.filename, "Files parse incorrectly")
        self.assertEqual(0, outside.id, "Files parse incorrectly")
        self.assertEqual("UTF-8", outside.__encoding__, "Encoding parse incorrectly")
        self.assertEqual("\\r\\n", outside.__lines_end__, "Lines end parse incorrectly")
        self.assertEqual("\\t", outside.__fields_end__, "Field end parse incorrectly")
        self.assertEqual("", outside.__fields_enclosed__, "Field enclosed parse incorrectly")
        self.assertEqual([1], outside.__ignore_header__, "Ignore header parse incorrectly")
        self.assertEqual("http://rs.gbif.org/terms/1.0/SpeciesProfile", outside.uri, "Row type parse incorrectly")
        self.assertEqual(5, len(outside.__fields__), "Fields parse incorrectly")
        outside.set_tag("extension")
        self.assertEqualTree(self.outside_xml, outside.to_element(), "Error on element conversion")

    def test_none(self):
        self.assertIsNone(OutsideClass.parse(None, {}), "Object parsed from nothing")

    def test_parse_invalid(self):
        self.assertRaises(
            AssertionError,
            OutsideClass.from_string,
            '<extension />'
        )


if __name__ == '__main__':
    unittest.main()
