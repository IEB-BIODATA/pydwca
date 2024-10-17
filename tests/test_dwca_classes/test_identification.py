import os.path
import unittest

from lxml import etree as et

from dwca.classes import Identification
from dwca.terms import TaxonID
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

    def test_name(self):
        taxon = Identification.from_string(self.text)
        self.assertEqual("Identification", taxon.name, "Name parsed incorrectly.")


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

    def test_set_core_field(self):
        identification = Identification.from_string(self.text)
        self.assertEqual("", identification.fields[0], "Field from nowhere.")
        identification.set_core_field(TaxonID(3))
        self.assertEqual(TaxonID(3).uri, identification.fields[0], "Field not set.")
        self.assertEqual(0, identification.__fields__[0].index, "Field not changed on set.")

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

    def test_sql_error(self):
        identification = Identification.from_string(self.text)
        with self.assertRaisesRegex(RuntimeError, "Extension"):
            _ = identification.sql_table
        identification.set_primary_key("Taxon")
        with self.assertRaisesRegex(RuntimeError, "Extension"):
            _ = identification.sql_table

    def test_set_primary_key(self):
        identification = Identification.from_string(self.text)
        self.assertIsNone(identification.__primary_key__, "Primary key from nowhere.")
        identification.set_primary_key("Taxon")
        self.assertIsNotNone(identification.__primary_key__, "Primary key not set.")
        self.assertEqual("Taxon", identification.__primary_key__, "Incorrect Primary key.")

    def test_sql_table(self):
        identification = Identification.from_string(self.text)
        identification.set_primary_key("Taxon")
        identification.set_core_field(TaxonID(3))
        self.assertEqual(
            self.normalize_sql("""
            CREATE TABLE "Identification" (
                "taxonID" VARCHAR,
                "identificationID" VARCHAR,
                "verbatimIdentification" VARCHAR,
                "identificationQualifier" VARCHAR,
                "typeStatus" VARCHAR,
                "identifiedBy" VARCHAR,
                "identifiedByID" VARCHAR,
                "dateIdentified" VARCHAR,
                "identificationReferences" VARCHAR,
                "identificationVerificationStatus" VARCHAR,
                "identificationRemarks" VARCHAR,
                "datasetID" VARCHAR,
                "subject" VARCHAR,
                PRIMARY KEY ("taxonID"),
                FOREIGN KEY ("taxonID") REFERENCES "Taxon"
            );
            """),
            self.normalize_sql(identification.sql_table),
            "Wrong SQL table."
        )


if __name__ == '__main__':
    unittest.main()
