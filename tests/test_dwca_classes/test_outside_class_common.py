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

    def __test_insert__(self):
        text_1 = """
        <extension encoding="UTF-8" linesTerminatedBy="\\n" fieldsTerminatedBy="\\t" fieldsEnclosedBy="" ignoreHeaderLines="1" rowType="http://example.org/terms/extension1">
        <files>
            <location>extension1.txt</location>
        </files>
        <coreid index="0" /><field index="1" term="http://example.org/terms/column1"/>
        <field index="2" term="http://example.org/terms/column2"/>
        </extension>
        """
        extension1 = OutsideClass.from_string(text_1)
        with self.assertRaisesRegex(
            RuntimeError,
            "Extension",
        ):
            next(extension1.insert_sql)
        extension1.set_core_field(TaxonID(5))
        with open(
                os.path.join(PATH, os.pardir, "example_data", "extension_example1.txt"),
                "r", encoding="utf-8"
        ) as file:
            extension1.read_file(file.read())
        text_2 = """
        <extension encoding="UTF-8" linesTerminatedBy="\\n" fieldsTerminatedBy="\\t" fieldsEnclosedBy="" ignoreHeaderLines="1" rowType="http://example.org/terms/extension2">
        <files>
          <location>extension2.txt</location>
        </files>
        <coreid index="0" /><field index="1" term="http://example.org/terms/column1"/>
        </extension>
        """
        extension2 = OutsideClass.from_string(text_2)
        extension2.set_core_field(TaxonID(5))
        with open(
                os.path.join(PATH, os.pardir, "example_data", "extension_example2.txt"),
                "r", encoding="utf-8"
        ) as file:
            extension2.read_file(file.read())
        expected_values_1 = [
            ("urn:lsid:example.org:taxname:0", "true", "false"),
            ("urn:lsid:example.org:taxname:8", "false", "true"),
            ("urn:lsid:example.org:taxname:19", "true", "true")
        ]
        self.assertEqual(3, len(list(extension1.insert_sql)), "Not the right amount of rows.")
        for (statement, values), expected in zip(extension1.insert_sql, expected_values_1):
            self.assertEqual(
                self.normalize_sql("""
                INSERT INTO "extension1" (
                    "taxonID",
                    "column1",
                    "column2"
                ) VALUES (%s, %s, %s)
                """), self.normalize_sql(statement), "Statement do not match"
            )
            self.assertEqual(expected, values, "Values do not match")
        expected_values_2 = [
            ("urn:lsid:example.org:taxname:20", "true"),
            ("urn:lsid:example.org:taxname:27", "true"),
            ("urn:lsid:example.org:taxname:41", "false")
        ]
        self.assertEqual(3, len(list(extension2.insert_sql)), "Not the right amount of rows.")
        for (statement, values), expected in zip(extension2.insert_sql, expected_values_2):
            self.assertEqual(
                self.normalize_sql("""
                INSERT INTO "extension2" (
                    "taxonID",
                    "column1"
                ) VALUES (%s, %s)
                """), self.normalize_sql(statement), "Statement do not match"
            )
            self.assertEqual(expected, values, "Values do not match")


if __name__ == '__main__':
    unittest.main()
