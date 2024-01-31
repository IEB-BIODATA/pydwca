import unittest
import lxml.etree as et

from eml.types import EMLAddress
from test_xml.test_xml import TestXML


class TestEMLAddress(TestXML):
    def test_parse(self):
        return

    def test_element(self):
        return

    def test_reference(self):
        reference_dataset_xml = """
<address>
    <references>1</references>
</dataset>
        """
        eml_dataset = EMLAddress.from_string(reference_dataset_xml)
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
        eml_dataset = EMLAddress.from_string(reference_dataset_xml)
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
            EMLAddress.from_string,
            reference_dataset_xml
        )


if __name__ == '__main__':
    unittest.main()
