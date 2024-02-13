import os
import unittest
from lxml import etree as et

from dwca.utils import Language
from eml.resources import EMLDataset
from eml.types import Scope
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestEMLDataset(TestXML):
    DEFAULT_TAGS = {
        "scope": "document",
        "{http://www.w3.org/XML/1998/namespace}lang": "eng",
        "phonetype": "voice",
    }

    def setUp(self) -> None:
        with open(os.path.join(PATH, os.pardir, "example_data", "eml.xml"), "r", encoding="utf-8") as file:
            content = file.read()
        base_file = et.fromstring(content)
        self.dataset_xml = base_file.find("dataset", namespaces=base_file.nsmap)
        self.text = et.tostring(self.dataset_xml, pretty_print=True).decode("utf-8")
        return

    def test_parse(self):
        dataset = EMLDataset.from_string(self.text)
        self.assertIsNone(dataset.id, "Id from nothing")
        self.assertIsNone(dataset.system, "System from nothing")
        self.assertEqual(Scope.DOCUMENT, dataset.scope, "Not given different than default")
        self.assertFalse(dataset.referencing, "Reference from nothing")
        self.assertEqual(1, len(dataset.titles), "Extra titles from nowhere")
        self.assertEqualTree(self.dataset_xml, dataset.to_element(), "Wrong element generated")
        return

    def test_missing_title(self):
        dataset_xml = """
<dataset>
    <alternativeIdentifier system="http://gbif.org">VCR3465</alternativeIdentifier>
    <shortName>A short description</shortName>
</dataset>
        """
        self.assertRaises(
            ValueError,
            EMLDataset.from_string,
            dataset_xml
        )

    def test_more_titles(self):
        dataset_xml = """
<dataset>
    <title>A Title</title>
    <title xml:lang="esp">Un Título</title>
    <title xml:lang="esp">Un Título Diferente</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternativeIdentifier system="http://gbif.org">VCR3465</alternativeIdentifier>
    <shortName>A short description</shortName>
    <contact>
        <organizationName>Organization Contact</organizationName>
    </contact>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(dataset_xml)
        self.assertNotEqual("Un Título", eml_dataset.title, "Title set in wrong order")
        self.assertEqual("A Title", eml_dataset.title, "Title not set")
        self.assertEqual("Un Título Diferente", eml_dataset.titles[2], "Extra titles set in wrong order")
        self.assertEqual(Language.ENG, eml_dataset.title.language, "Title set in wrong language")
        self.assertEqualTree(et.fromstring(dataset_xml), eml_dataset.to_element(), "Wrong to element")

    def test_alternative_identifier(self):
        dataset_xml = """
<dataset>
    <title xml:lang="eng">Test Title</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternativeIdentifier system="http://gbif.org">VCR3465</alternativeIdentifier>
    <shortName>A short description</shortName>
    <contact>
        <organizationName>Organization Contact</organizationName>
    </contact>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(dataset_xml)
        self.assertEqual("VCR3465", eml_dataset.alternative_identifiers[0], "Alternative id set incorrectly")
        self.assertEqual("http://gbif.org", eml_dataset.alternative_identifiers[0].system,
                         "Alternative id set incorrectly")
        self.assertEqual("A short description", eml_dataset.short_name,
                         "Short name not set correctly")
        self.assertEqualTree(
            et.fromstring(dataset_xml),
            eml_dataset.to_element(),
            "Wrong alternative identifier to element"
        )

    def test_alternative_identifiers(self):
        dataset_xml = """
<dataset>
    <title>Title</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternativeIdentifier system="http://gbif.org">VCR3465</alternativeIdentifier>
    <alternativeIdentifier>VCR3465</alternativeIdentifier>
    <contact>
        <organizationName>Organization Contact</organizationName>
    </contact>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(dataset_xml)
        self.assertEqual("VCR3465", eml_dataset.alternative_identifiers[0], "Alternative id set incorrectly")
        self.assertEqual("http://gbif.org", eml_dataset.alternative_identifiers[0].system,
                         "Alternative id set incorrectly")
        self.assertEqual("VCR3465", eml_dataset.alternative_identifiers[1], "Alternative system set incorrectly")
        self.assertIsNone(eml_dataset.alternative_identifiers[1].system, "Alternative system set incorrectly")
        self.assertEqualTree(
            et.fromstring(dataset_xml),
            eml_dataset.to_element(),
            "Wrong alternative identifiers to element"
        )

    def test_reference_dataset(self):
        reference_dataset_xml = """
<dataset>
    <references>1</references>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(reference_dataset_xml)
        self.assertEqual("1", eml_dataset.id, "Id set incorrectly")
        self.assertTrue(eml_dataset.referencing, "Referencing wrong initialized")
        self.assertIsNone(
            eml_dataset.references.system,
            "References system wrong initialized"
        )
        self.assertEqualTree(
            et.fromstring(reference_dataset_xml),
            eml_dataset.to_element(),
            "Wrong referrer to element"
        )

    def test_reference_system(self):
        reference_dataset_xml = """
<dataset>
    <references system="http://gbif.org">1</references>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(reference_dataset_xml)
        self.assertEqual("1", eml_dataset.id, "Id set incorrectly")
        self.assertTrue(eml_dataset.referencing, "Referencing wrong initialized")
        self.assertEqual(
            "http://gbif.org",
            eml_dataset.references.system,
            "References system wrong initialized"
        )
        self.assertEqualTree(
            et.fromstring(reference_dataset_xml),
            eml_dataset.to_element(),
            "Wrong referrer to element"
        )

    def test_invalid_reference(self):
        reference_dataset_xml = """
<dataset id="10">
    <references>1</references>
</dataset>
        """
        self.assertRaises(
            AssertionError,
            EMLDataset.from_string,
            reference_dataset_xml
        )


if __name__ == '__main__':
    unittest.main()
