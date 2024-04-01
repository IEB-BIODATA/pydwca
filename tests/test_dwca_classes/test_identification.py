import os.path
import unittest

from lxml import etree as et

from dwca.classes import Identification
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestIdentification(TestXML):
    def setUp(self) -> None:
        with open(os.path.join(PATH, os.pardir, "example_data", "meta.xml"), "r", encoding="utf-8") as file:
            content = file.read()
        base_file = et.fromstring(content)
        self.identification_xml = base_file.findall("extension", namespaces=base_file.nsmap)[2]
        self.text = et.tostring(self.identification_xml, pretty_print=True).decode("utf-8")
        return

    def test_parse(self):
        identification = Identification.from_string(self.text)
        self.assertEqual("identification.txt", identification.filename, "Files parse incorrectly")
        self.assertEqual(0, identification.id, "Files parse incorrectly")
        self.assertEqual("UTF-8", identification.__encoding__, "Encoding parse incorrectly")
        self.assertEqual("\n", identification.__lines_end__, "Lines end parse incorrectly")
        self.assertEqual("\t", identification.__fields_end__, "Field end parse incorrectly")
        self.assertEqual("", identification.__fields_enclosed__, "Field enclosed parse incorrectly")
        self.assertEqual(1, identification.__ignore_header_lines__, "Ignore header parse incorrectly")
        self.assertEqual(Identification.URI, identification.uri, "Row type parse incorrectly")
        self.assertEqual(13, len(identification.__fields__), "Fields parse incorrectly")
        self.assertEqualTree(self.identification_xml, identification.to_element(), "Error on element conversion")

    def test_none(self):
        self.assertIsNone(Identification.parse(None, {}), "Object parsed from nothing")

    def test_missing_field(self):
        self.assertRaises(
            AssertionError,
            Identification.from_string,
            """
<core>
    <files>
      <location>missing.txt</location>
    </files>
    <id index="0"/>
    <field index="0" term=""/>
    <field index="1" term=""/>
    <field index="3" term=""/>
</core>
            """
        )

    def test_field_twice(self):
        self.assertRaises(
            AssertionError,
            Identification.from_string,
            """
<core>
    <files>
      <location>missing.txt</location>
    </files>
    <id index="0"/>
    <field index="0" term=""/>
    <field index="1" term=""/>
    <field index="3" term=""/>
    <field index="2" term=""/>
    <field index="3" term=""/>
    <field index="4" term=""/>
</core>
            """
        )

    def test_parse_invalid(self):
        self.assertRaises(
            AssertionError,
            Identification.from_string,
            '<extension />'
        )
        self.assertRaises(
            KeyError,
            Identification.from_string,
            """
<core-id>
    <field index="0" term=""/>
</core-id>
            """
        )


if __name__ == '__main__':
    unittest.main()
