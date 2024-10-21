import os.path
import unittest
from typing import Tuple

from lxml import etree as et

from dwca.classes import OutsideClass
from dwca.terms import TaxonID
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestOutsideCommon(TestXML):
    @staticmethod
    def read_xml(path: str) -> Tuple[str, str]:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        base_file = et.fromstring(content)
        outside_xml = base_file.findall("extension", namespaces=base_file.nsmap)[0]
        text = et.tostring(outside_xml, pretty_print=True).decode("utf-8")
        return outside_xml, text

    def setUp(self) -> None:
        self.outside_xml, self.text = self.read_xml(os.path.join(PATH, os.pardir, "example_data", "meta.xml"))
        return

    def __test_parse__(self):
        outside = OutsideClass.from_string(self.text)
        self.assertEqual("speciesprofile.txt", outside.filename, "Files parse incorrectly")
        self.assertEqual(0, outside.id, "Files parse incorrectly")
        self.assertEqual("UTF-8", outside.__encoding__, "Encoding parse incorrectly")
        self.assertEqual("\n", outside.__lines_end__, "Lines end parse incorrectly")
        self.assertEqual("\t", outside.__fields_end__, "Field end parse incorrectly")
        self.assertEqual("", outside.__fields_enclosed__, "Field enclosed parse incorrectly")
        self.assertEqual(1, outside.__ignore_header_lines__, "Ignore header parse incorrectly")
        self.assertEqual("http://rs.gbif.org/terms/1.0/SpeciesProfile", outside.uri, "Row type parse incorrectly")
        self.assertEqual(5, len(outside.__fields__), "Fields parse incorrectly")
        self.assertEqualTree(self.outside_xml, outside.to_element(), "Error on element conversion")

    def __test_none__(self):
        self.assertIsNone(OutsideClass.parse(None, {}), "Object parsed from nothing")

    def __test_merge__(self):
        xml_file_1, text_1 = self.read_xml(os.path.join(PATH, os.pardir, "example_data", "dataset1_meta.xml"))
        xml_file_2, text_2 = self.read_xml(os.path.join(PATH, os.pardir, "example_data", "dataset2_meta.xml"))
        extension1 = OutsideClass.from_string(text_1)
        with open(
                os.path.join(PATH, os.pardir, "example_data", "extension_example1.txt"),
                "r", encoding="utf-8"
        ) as file:
            extension1.read_file(file.read())
        extension2 = OutsideClass.from_string(text_2)
        with open(
                os.path.join(PATH, os.pardir, "example_data", "extension_example2.txt"),
                "r", encoding="utf-8"
        ) as file:
            extension2.read_file(file.read())
        merged = OutsideClass.merge(extension1, extension2)
        self.assertEqual(len(merged), len(extension1) + len(extension2), "Incorrect merged of taxa files.")
        self.assertCountEqual(
            merged.fields,
            extension1.fields,
            "Incorrect number of fields"
        )

    def __test_set_primary_key__(self):
        outside_class = OutsideClass.from_string(self.text)
        self.assertIsNone(outside_class.__primary_key__, "Primary key from nowhere.")
        outside_class.set_primary_key("Taxon")
        self.assertIsNotNone(outside_class.__primary_key__, "Primary key not set.")
        self.assertEqual("Taxon", outside_class.__primary_key__, "Incorrect Primary key.")

    def __test_sql_table__(self):
        self.outside_xml, self.text = self.read_xml(os.path.join(PATH, os.pardir, "example_data", "meta.xml"))
        outside_class = OutsideClass.from_string(self.text)
        with self.assertRaisesRegex(
            RuntimeError,
            "Extension",
        ):
            _ = outside_class.sql_table
        outside_class.set_primary_key("Taxon")
        with self.assertRaisesRegex(
            RuntimeError,
            "Extension",
        ):
            _ = outside_class.sql_table
        outside_class.set_core_field(TaxonID(5))
        self.assertEqual(self.normalize_sql("""
        CREATE TABLE "SpeciesProfile" (
            "taxonID" VARCHAR,
            "isMarine" VARCHAR,
            "isFreshwater" VARCHAR,
            "isTerrestrial" VARCHAR,
            "isExtinct" VARCHAR,
            PRIMARY KEY ("taxonID"),
            FOREIGN KEY ("taxonID") REFERENCES "Taxon"
        );
        """), self.normalize_sql(outside_class.sql_table), "Wrong SQL table.")


if __name__ == '__main__':
    unittest.main()
