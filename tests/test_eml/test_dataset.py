import os
import unittest
from lxml import etree as et

from xml_common.utils import Language
from eml.resources import EMLDataset
from eml.types import Scope, SemanticAnnotation
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
        self.assertEqual(
            """\tTitle: Example for Darwin Core Archive
\tCreator: Creator Organization
\tMetadataProvider: Metadata Manager at Metadata Provider Organization
\tCustodian Steward: Doe, J. (Custodian Steward)
\tOriginator: Doe, J.
\tAuthor: Example, J.""",
            str(dataset),
            "Error on parse to string"
        )
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
    <alternateIdentifier system="http://gbif.org">VCR3465</alternateIdentifier>
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
    <title xml:lang="spa">Un Título</title>
    <title xml:lang="spa">Un Título Diferente</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternateIdentifier system="http://gbif.org">VCR3465</alternateIdentifier>
    <shortName>A short description</shortName>
    <contact>
        <organizationName>Organization Contact</organizationName>
    </contact>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(dataset_xml)
        self.assertNotEqual("Un Título", eml_dataset.title, "Title set in wrong order.")
        self.assertEqual("A Title", eml_dataset.title, "Title not set.")
        self.assertEqual("Un Título Diferente", eml_dataset.titles[2], "Extra titles set in wrong order.")
        self.assertEqual(Language.ENG, eml_dataset.title.language, "Title set in wrong language.")
        self.assertEqualTree(et.fromstring(dataset_xml), eml_dataset.to_element(), "Wrong to element.")

    def test_alternate_identifier(self):
        dataset_xml = """
<dataset>
    <title xml:lang="eng">Test Title</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternateIdentifier system="http://gbif.org">VCR3465</alternateIdentifier>
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

    def test_alternate_identifiers(self):
        dataset_xml = """
<dataset>
    <title>Title</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternateIdentifier system="http://gbif.org">VCR3465</alternateIdentifier>
    <alternateIdentifier>VCR3465</alternateIdentifier>
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

    def test_annotate_invalid(self):
        dataset = EMLDataset.from_string(self.text)
        self.assertEqual(0, len(dataset.annotation), "Annotation from nowhere")
        self.assertRaises(
            ValueError,
            dataset.annotate,
            SemanticAnnotation(
                (
                    "http://ecoinformatics.org/oboe/oboe.1.2/oboe-characteristics.owl#ofCharacteristic",
                    "has characteristic"
                ),(
                    "http://ecoinformatics.org/oboe/oboe.1.2/oboe-characteristics.owl#Mass",
                    "Mass"
                )
            )
        )

    def test_annotate(self):
        dataset = EMLDataset.from_string(self.text)
        dataset.__id__ = "1"
        self.assertEqual(0, len(dataset.annotation), "Annotation from nowhere")
        annotation = SemanticAnnotation(
            ("http://ecoinformatics.org/oboe/oboe.1.2/oboe-characteristics.owl#ofCharacteristic", "has characteristic"),
            ("http://ecoinformatics.org/oboe/oboe.1.2/oboe-characteristics.owl#Mass", "Mass")
        )
        dataset.annotate(annotation)
        self.assertEqual(1, len(dataset.annotation), "Annotation not set")
        text_as_element = et.fromstring(self.text)
        annotation.set_tag("annotation")
        text_as_element.set("id", "1")
        text_as_element.append(annotation.to_element())
        self.assertEqualTree(text_as_element, dataset.to_element(), "Annotation not set in element tree")

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

    def test_no_contact(self):
        dataset_xml = """
<dataset>
    <title>A Title</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternateIdentifier system="http://gbif.org">VCR3465</alternateIdentifier>
    <shortName>A short description</shortName>
</dataset>
        """
        with self.assertRaisesRegex(ValueError, "No contact provided."):
            EMLDataset.from_string(dataset_xml)
        return

    def test_purpose(self):
        dataset_xml = """
<dataset>
    <title>A Title</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternateIdentifier system="http://gbif.org">VCR3465</alternateIdentifier>
    <shortName>A short description</shortName>
    <purpose>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.</para>
    </purpose>
    <contact>
        <organizationName>Organization Contact</organizationName>
    </contact>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(dataset_xml)
        self.assertNotEqual("Un Título", eml_dataset.title, "Title set in wrong order.")
        self.assertEqual(Language.ENG, eml_dataset.title.language, "Title set in wrong language,")
        self.assertEqual("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.", eml_dataset.purpose.paragraphs[0], "Purpose not parsed.")
        self.assertEqualTree(et.fromstring(dataset_xml), eml_dataset.to_element(), "Wrong to element.")

    def test_intro(self):
        dataset_xml = """
<dataset>
    <title>A Title</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternateIdentifier system="http://gbif.org">VCR3465</alternateIdentifier>
    <shortName>A short description</shortName>
    <introduction>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.</para>
    </introduction>
    <contact>
        <organizationName>Organization Contact</organizationName>
    </contact>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(dataset_xml)
        self.assertNotEqual("Un Título", eml_dataset.title, "Title set in wrong order.")
        self.assertEqual(Language.ENG, eml_dataset.title.language, "Title set in wrong language,")
        self.assertEqual("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.",
                         eml_dataset.introduction.paragraphs[0], "Introduction not parsed.")
        self.assertEqualTree(et.fromstring(dataset_xml), eml_dataset.to_element(), "Wrong to element.")

    def test_getting_started(self):
        dataset_xml = """
<dataset>
    <title>A Title</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternateIdentifier system="http://gbif.org">VCR3465</alternateIdentifier>
    <shortName>A short description</shortName>
    <gettingStarted>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.</para>
    </gettingStarted>
    <contact>
        <organizationName>Organization Contact</organizationName>
    </contact>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(dataset_xml)
        self.assertNotEqual("Un Título", eml_dataset.title, "Title set in wrong order.")
        self.assertEqual(Language.ENG, eml_dataset.title.language, "Title set in wrong language,")
        self.assertEqual("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.",
                         eml_dataset.getting_started.paragraphs[0], "Getting Started not parsed.")
        self.assertEqualTree(et.fromstring(dataset_xml), eml_dataset.to_element(), "Wrong to element.")

    def test_acknowledgements(self):
        dataset_xml = """
<dataset>
    <title>A Title</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternateIdentifier system="http://gbif.org">VCR3465</alternateIdentifier>
    <shortName>A short description</shortName>
    <acknowledgements>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.</para>
    </acknowledgements>
    <contact>
        <organizationName>Organization Contact</organizationName>
    </contact>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(dataset_xml)
        self.assertNotEqual("Un Título", eml_dataset.title, "Title set in wrong order.")
        self.assertEqual(Language.ENG, eml_dataset.title.language, "Title set in wrong language,")
        self.assertEqual("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.",
                         eml_dataset.acknowledgements.paragraphs[0], "Acknowledgements not parsed.")
        self.assertEqualTree(et.fromstring(dataset_xml), eml_dataset.to_element(), "Wrong to element.")

    def test_maintenance(self):
        dataset_xml = """
<dataset>
    <title>A Title</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternateIdentifier system="http://gbif.org">VCR3465</alternateIdentifier>
    <shortName>A short description</shortName>
    <maintenance>
        <description>
            <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.</para>
        </description>
    </maintenance>
    <contact>
        <organizationName>Organization Contact</organizationName>
    </contact>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(dataset_xml)
        self.assertNotEqual("Un Título", eml_dataset.title, "Title set in wrong order.")
        self.assertEqual(Language.ENG, eml_dataset.title.language, "Title set in wrong language,")
        self.assertEqual("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.",
                         eml_dataset.maintenance.description.paragraphs[0], "Maintenance not parsed.")
        self.assertEqualTree(et.fromstring(dataset_xml), eml_dataset.to_element(), "Wrong to element.")

    def test_publisher(self):
        dataset_xml = """
<dataset>
    <title>A Title</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternateIdentifier system="http://gbif.org">VCR3465</alternateIdentifier>
    <shortName>A short description</shortName>
    <contact>
        <organizationName>Organization Contact</organizationName>
    </contact>
    <publisher>
        <organizationName>Organization Publisher</organizationName>
    </publisher>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(dataset_xml)
        self.assertNotEqual("Un Título", eml_dataset.title, "Title set in wrong order.")
        self.assertEqual(Language.ENG, eml_dataset.title.language, "Title set in wrong language,")
        self.assertEqual("Organization Publisher",
                         str(eml_dataset.publisher.organization_name),
                         "Publisher not parsed.")
        self.assertEqualTree(et.fromstring(dataset_xml), eml_dataset.to_element(), "Wrong to element.")

    def test_pub_place(self):
        dataset_xml = """
<dataset>
    <title>A Title</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternateIdentifier system="http://gbif.org">VCR3465</alternateIdentifier>
    <shortName>A short description</shortName>
    <contact>
        <organizationName>Organization Contact</organizationName>
    </contact>
    <pubPlace>San Francisco, CA, USA</pubPlace>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(dataset_xml)
        self.assertNotEqual("Un Título", eml_dataset.title, "Title set in wrong order.")
        self.assertEqual(Language.ENG, eml_dataset.title.language, "Title set in wrong language,")
        self.assertEqual("San Francisco, CA, USA",
                         str(eml_dataset.pub_place),
                         "Publication place not parsed.")
        self.assertEqualTree(et.fromstring(dataset_xml), eml_dataset.to_element(), "Wrong to element.")

    def test_methods(self):
        dataset_xml = """
<dataset>
    <title>A Title</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternateIdentifier system="http://gbif.org">VCR3465</alternateIdentifier>
    <shortName>A short description</shortName>
    <contact>
        <organizationName>Organization Contact</organizationName>
    </contact>
    <methods>
        <methodStep>
            <description>
                <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.</para>
            </description>
        </methodStep>
    </methods>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(dataset_xml)
        self.assertNotEqual("Un Título", eml_dataset.title, "Title set in wrong order.")
        self.assertEqual(Language.ENG, eml_dataset.title.language, "Title set in wrong language,")
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.",
            eml_dataset.methods.method_steps[0].description.paragraphs[0],
            "Methods not parsed."
        )
        self.assertEqualTree(et.fromstring(dataset_xml), eml_dataset.to_element(), "Wrong to element.")

    def test_project(self):
        dataset_xml = """
<dataset>
    <title>A Title</title>
    <creator>
        <organizationName>Organization Creator</organizationName>
    </creator>
    <alternateIdentifier system="http://gbif.org">VCR3465</alternateIdentifier>
    <shortName>A short description</shortName>
    <contact>
        <organizationName>Organization Contact</organizationName>
    </contact>
    <project>
        <title>Example Title</title>
        <personnel>
            <organizationName>Example Organization</organizationName>
            <role>contentProvider</role>
        </personnel>
    </project>
</dataset>
        """
        eml_dataset = EMLDataset.from_string(dataset_xml)
        self.assertNotEqual("Un Título", eml_dataset.title, "Title set in wrong order.")
        self.assertEqual(Language.ENG, eml_dataset.title.language, "Title set in wrong language,")
        self.assertEqual(
            "Example Title",
            eml_dataset.project.title,
            "Project not parsed."
        )
        self.assertEqualTree(et.fromstring(dataset_xml), eml_dataset.to_element(), "Wrong to element.")


if __name__ == '__main__':
    unittest.main()
