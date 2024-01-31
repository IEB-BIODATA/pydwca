import os
import unittest
import lxml.etree as et

from eml.types import ResponsibleParty
from test_xml.test_xml import TestXML


class TestResponsibleParty(TestXML):
    def setUp(self) -> None:
        with open(os.path.join(os.pardir, "example_data", "eml.xml"), "r", encoding="utf-8") as file:
            content = file.read()
        base_file = et.fromstring(content)
        self.nmap = base_file.nmap
        self.dataset_xml = base_file.find("dataset", namespaces=base_file.nsmap)
        return

    def test_parse_creator(self):
        xml = self.dataset_xml.find("creator", namespaces=self.nmap)
        text = et.tostring(xml, pretty_print=True).decode("utf-8")
        resp_party = ResponsibleParty.from_string(text)
        self.assertEqual("Rees, T. (compiler)", resp_party.organization_name, "Error on parsing organization name")
        self.assertEqual("info@irmng.org", resp_party.mail, "Error on parsing electronic mail address")
        self.assertEqual(None, resp_party.address, "Error on parsing address")
        self.assertEqual("https://www.irmng.org", resp_party.url, "Error on parsing online url")
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
            "WoRMS Data Management Team (DMT)",
            resp_party.organization_name,
            "Error on parsing organization name"
        )
        self.assertEqual("info@irmng.org", resp_party.mail, "Error on parsing electronic mail address")
        self.assertEqual(None, resp_party.address, "Error on parsing address")
        self.assertEqual("https://www.irmng.org", resp_party.url, "Error on parsing online url")
        resp_party.set_tag("metadataProvider")
        self.assertEqualTree(et.fromstring(text), resp_party.to_element(), "Metadata Provider error on to element")

    def test_parse_associated_party(self):
        xml = self.dataset_xml.find("associatedParty", namespaces=self.nmap)
        text = et.tostring(xml, pretty_print=True).decode("utf-8")
        resp_party = ResponsibleParty.from_string(text)
        self.assertEqual("Vandepitte, L", str(resp_party.individual_name), "Error on parsing individual name")
        self.assertEqual(
            "Vlaams Instituut voor de Zee",
            resp_party.organization_name,
            "Error on parsing organization name"
        )
        self.assertEqual("leen.vandepitte@vliz.be", resp_party.mail, "Error on parsing electronic mail address")
        self.assertEqual(None, resp_party.address, "Error on parsing address")

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
        eml_dataset = ResponsibleParty.from_string(reference_xml)
        self.assertEqual("1", eml_dataset.id, "Id set incorrectly")
        self.assertTrue(eml_dataset.referencing, "Referencing wrong initialized")
        self.assertEqual(
            "http://gbif.org",
            eml_dataset.references.system,
            "References system wrong initialized"
        )
        self.assertEqualTree(
            et.fromstring(reference_xml),
            eml_dataset.to_element(),
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


if __name__ == '__main__':
    unittest.main()
