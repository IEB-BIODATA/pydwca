import logging
import os
import unittest
from lxml import etree as et

from eml.types import ResponsibleParty, EMLAddress, IndividualName, PositionName, OrganizationName
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestResponsibleParty(TestXML):
    DEFAULT_TAGS = {
        "{http://www.w3.org/XML/1998/namespace}lang": "eng",
        "scope": "document",
        "phonetype": "voice",
    }

    def setUp(self) -> None:
        logging.getLogger().setLevel(logging.DEBUG)
        with open(os.path.join(PATH, os.pardir, "example_data", "eml.xml"), "r", encoding="utf-8") as file:
            content = file.read()
        base_file = et.fromstring(content)
        self.nmap = base_file.nsmap
        self.dataset_xml = base_file.find("dataset", namespaces=base_file.nsmap)
        self.individual = IndividualName(first_name="John", last_name="Doe")
        self.position = PositionName("Digitizer")
        self.organization = OrganizationName("Example Organization")
        return

    def test_parse_creator(self):
        xml = self.dataset_xml.find("creator", namespaces=self.nmap)
        text = et.tostring(xml, pretty_print=True).decode("utf-8")
        resp_party = ResponsibleParty.from_string(text)
        self.assertEqual("Creator Organization", resp_party.organization_name, "Error on parsing organization name")
        self.assertEqual("info@creator.org", resp_party.mail[0], "Error on parsing electronic mail address")
        self.assertEqual("https://example.creator.org", resp_party.url[0], "Error on parsing online url")
        self.assertRaises(
            RuntimeError,
            resp_party.to_element
        )
        resp_party.set_tag("creator")
        self.assertEqualTree(et.fromstring(text), resp_party.to_element(), "Creator error on to element")

    def test_parse_metadata_provider(self):
        xml = self.dataset_xml.find("metadataProvider", namespaces=self.nmap)
        text = et.tostring(xml, pretty_print=True).decode("utf-8")
        resp_party = ResponsibleParty.from_string(text)
        self.assertEqual(
            "Metadata Provider Organization",
            resp_party.organization_name,
            "Error on parsing organization name"
        )
        self.assertEqual(
            "Metadata Manager",
            resp_party.position_name,
            "Error on parsing position name"
        )
        self.assertEqual("info@metadata.org", resp_party.mail[0], "Error on parsing electronic mail address")
        self.assertEqual(
            EMLAddress(city="Ostend", postal_code="4568", country="BE"),
            resp_party.address[0],
            "Error on parsing address"
        )
        self.assertEqual("https://example.metadata.org", resp_party.url[0], "Error on parsing online url")
        resp_party.set_tag("metadataProvider")
        self.assertEqualTree(et.fromstring(text), resp_party.to_element(), "Metadata Provider error on to element")

    def test_parse_associated_party(self):
        xml = self.dataset_xml.find("associatedParty", namespaces=self.nmap)
        text = et.tostring(xml, pretty_print=True).decode("utf-8")
        resp_party = ResponsibleParty.from_string(text)
        self.assertEqual("Doe, J.", str(resp_party.individual_name), "Error on parsing individual name")
        self.assertEqual(
            "Custodian Steward",
            resp_party.organization_name,
            "Error on parsing organization name"
        )
        self.assertEqual("info@custodian.org", resp_party.mail[0], "Error on parsing electronic mail address")
        self.assertEqual(EMLAddress(country="Belgium"), resp_party.address[0], "Error on parsing address")
        self.assertEqual("486554390", resp_party.phone[0], "Error on parsing phone")
        resp_party.set_tag("associatedParty")
        text = text.replace("<role>custodianSteward</role>", "")
        self.assertEqualTree(et.fromstring(text), resp_party.to_element(), "Wrong to element")

    def test_reference_resp_party(self):
        reference_xml = """
<creator>
    <references>1</references>
</creator>
        """
        eml_resp_party = ResponsibleParty.from_string(reference_xml)
        self.assertEqual("1", eml_resp_party.id, "Id set incorrectly")
        self.assertTrue(eml_resp_party.referencing, "Referencing wrong initialized")
        self.assertIsNone(
            eml_resp_party.references.system,
            "References system wrong initialized"
        )
        eml_resp_party.set_tag("creator")
        self.assertEqualTree(
            et.fromstring(reference_xml),
            eml_resp_party.to_element(),
            "Wrong referrer to element"
        )

    def test_reference_system(self):
        reference_xml = """
<creator>
    <references system="http://gbif.org">1</references>
</creator>
        """
        eml_resp_party = ResponsibleParty.from_string(reference_xml)
        self.assertEqual("1", eml_resp_party.id, "Id set incorrectly")
        self.assertTrue(eml_resp_party.referencing, "Referencing wrong initialized")
        self.assertEqual(
            "http://gbif.org",
            eml_resp_party.references.system,
            "References system wrong initialized"
        )
        self.assertRaises(
            RuntimeError,
            eml_resp_party.to_element
        )
        eml_resp_party.set_tag("creator")
        self.assertEqualTree(
            et.fromstring(reference_xml),
            eml_resp_party.to_element(),
            "Wrong referrer to element"
        )

    def test_invalid_reference(self):
        reference_xml = """
<creator id="10">
    <references>1</references>
</creator>
        """
        self.assertRaises(
            AssertionError,
            ResponsibleParty.from_string,
            reference_xml
        )

    def test_str_individual(self):
        just_individual = ResponsibleParty(individual_name=self.individual)
        self.assertEqual("Doe, J.", str(just_individual), "Error on string of individual.")
        individual_position = ResponsibleParty(
            individual_name=self.individual,
            position_name=self.position
        )
        self.assertEqual(
            "Doe, J. (Digitizer)",
            str(individual_position),
            "Error on string of individual with position."
        )
        individual_organization = ResponsibleParty(
            individual_name=self.individual,
            organization_name=self.organization
        )
        self.assertEqual(
            "Doe, J. (Example Organization)",
            str(individual_organization),
            "Error on string of individual with organization."
        )
        individual_complete = ResponsibleParty(
            individual_name=self.individual,
            position_name=self.position,
            organization_name=self.organization
        )
        self.assertEqual(
            "Doe, J. (Digitizer at Example Organization)",
            str(individual_complete),
            "Error on string of complete individual."
        )

    def test_str_position(self):
        just_position = ResponsibleParty(position_name=self.position)
        self.assertEqual("Digitizer", str(just_position), "Error on string of position.")
        position_organization = ResponsibleParty(
            position_name=self.position,
            organization_name=self.organization
        )
        self.assertEqual(
            "Digitizer at Example Organization",
            str(position_organization),
            "Error on string of position with organization."
        )

    def test_str_organization(self):
        just_organization = ResponsibleParty(organization_name=self.organization)
        self.assertEqual("Example Organization", str(just_organization), "Error on string of organization.")


if __name__ == '__main__':
    unittest.main()
