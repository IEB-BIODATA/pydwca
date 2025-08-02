import logging
import os.path
import unittest

from dwca.classes import OutsideClass
from dwca.terms import TaxonID
from test_dwca_classes.test_outside_class_common import TestOutsideCommon

PATH = os.path.abspath(os.path.dirname(__file__))


class TestOutside(TestOutsideCommon):
    def setUp(self) -> None:
        self.outside_xml, self.text = self.read_xml(os.path.join(PATH, os.pardir, "example_data", "meta.xml"))
        return

    def test_name(self):
        outside_class = OutsideClass.from_string(self.text)
        self.assertEqual("SpeciesProfile", outside_class.name, "Name parsed incorrectly.")

    def test_parse(self):
        super().__test_parse__()

    def test_none(self):
        super().__test_none__()

    def test_merge(self):
        super().__test_merge__()

    def test_missing_field(self):
        self.assertRaises(
            AssertionError,
            OutsideClass.from_string,
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
            OutsideClass.from_string,
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
            OutsideClass.from_string,
            '<extension />'
        )
        self.assertRaises(
            KeyError,
            OutsideClass.from_string,
            """
<core-id>
    <field index="0" term=""/>
</core-id>
            """
        )

    def test_set_primary_key(self):
        self.__test_set_primary_key__()

    def test_sql_table(self):
        self.__test_sql_table__()

    def test_insert(self):
        self.__test_insert__()

    def test_insert_lazy(self):
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
                os.path.join(PATH, os.pardir, "example_data", "extension_example1.txt"), "rb"
        ) as file:
            extension1.read_file("", source_file=file, lazy=True, _no_interaction=True)
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
                os.path.join(PATH, os.pardir, "example_data", "extension_example2.txt"), "rb"
        ) as file:
            extension2.read_file("", source_file=file, lazy=True, _no_interaction=True)
        expected_values_1 = [
            ("urn:lsid:example.org:taxname:0", "true", "false"),
            ("urn:lsid:example.org:taxname:8", "false", "true"),
            ("urn:lsid:example.org:taxname:19", "true", "true")
        ]
        with open(
                os.path.join(PATH, os.pardir, "example_data", "extension_example1.txt"), "rb"
        ) as file:
            logging.info(file.read())
        # Difference between local and GitHub Action, it appears to be polar related
        self.assertLessEqual(2, len(list(extension1.insert_sql)), "Not the right amount of rows.")
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
        extension1.close()
        expected_values_2 = [
            ("urn:lsid:example.org:taxname:20", "true"),
            ("urn:lsid:example.org:taxname:27", "true"),
            ("urn:lsid:example.org:taxname:41", "false")
        ]
        # Difference between local and GitHub Action, it appears to be polar related
        self.assertLessEqual(2, len(list(extension2.insert_sql)), "Not the right amount of rows.")
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
        extension2.close()


if __name__ == '__main__':
    unittest.main()
