import os.path
import unittest

from lxml import etree as et

from dwca.classes import Taxon
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestTaxon(TestXML):
    def setUp(self) -> None:
        with open(os.path.join(PATH, os.pardir, "example_data", "meta.xml"), "r", encoding="utf-8") as file:
            content = file.read()
        base_file = et.fromstring(content)
        self.taxon_xml = base_file.find("core", namespaces=base_file.nsmap)
        self.text = et.tostring(self.taxon_xml, pretty_print=True).decode("utf-8")
        self.taxon = None
        return

    def read_pandas(self):
        self.taxon = Taxon.from_string(self.text)
        with open(os.path.join(PATH, os.pardir, "example_data", "taxon.txt"), "r", encoding="utf-8") as file:
            self.taxon.read_file(file.read())
        return

    def test_parse(self):
        taxon = Taxon.from_string(self.text)
        self.assertEqual("taxon.txt", taxon.filename, "Files parse incorrectly")
        self.assertEqual(0, taxon.id, "Files parse incorrectly")
        self.assertEqual("UTF-8", taxon.__encoding__, "Encoding parse incorrectly")
        self.assertEqual("\n", taxon.__lines_end__, "Lines end parse incorrectly")
        self.assertEqual("\t", taxon.__fields_end__, "Field end parse incorrectly")
        self.assertEqual("", taxon.__fields_enclosed__, "Field enclosed parse incorrectly")
        self.assertEqual(1, taxon.__ignore_header_lines__, "Ignore header parse incorrectly")
        self.assertEqual(Taxon.URI, taxon.uri, "Row type parse incorrectly")
        self.assertEqual(47, len(taxon.__fields__), "Fields parse incorrectly")
        self.assertEqualTree(self.taxon_xml, taxon.to_element(), "Error on element conversion")

    def test_none(self):
        self.assertIsNone(Taxon.parse(None, {}), "Object parsed from nothing")

    def test_missing_field(self):
        self.assertRaises(
            AssertionError,
            Taxon.from_string,
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
            Taxon.from_string,
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
            Taxon.from_string,
            '<extension />'
        )
        self.assertRaises(
            KeyError,
            Taxon.from_string,
            """
<core-id>
    <field index="0" term=""/>
</core-id>
            """
        )

    def test_set_pandas(self):
        self.read_pandas()
        df = self.taxon.pandas
        self.assertEqual(163460, len(self.taxon), "Data incorrectly read.")
        self.assertEqual(163460, len(df), "DataFrame incorrectly read.")
        df = df[0:100]
        self.taxon.pandas = df
        self.assertEqual(100, len(df), "DataFrame incorrectly set.")
        self.assertEqual(100, len(self.taxon), "Data incorrectly set.")


if __name__ == '__main__':
    unittest.main()
