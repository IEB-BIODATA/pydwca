import unittest

from lxml import etree as et

from eml.resources import EMLCoverage
from test_xml.test_xml import TestXML


class TestCoverage(TestXML):
    DEFAULT_TAGS = {
        "scope": "document",
    }

    def test_parse_none(self):
        self.assertIsNone(EMLCoverage.parse(None, {}), "Distribution from nowhere")

    def test_parse(self):
        xml_text = """
<coverage id="1" scope="document">
    <geographicCoverage>
        <references>2</references>
    </geographicCoverage>
    <temporalCoverage>
        <references>3</references>
    </temporalCoverage>
    <taxonomicCoverage>
        <references>4</references>
    </taxonomicCoverage>
</coverage>
        """
        coverage = EMLCoverage.from_string(xml_text)
        self.assertEqual("1", coverage.id, "Error on parsing id")
        self.assertEqual(
            "2",
            coverage.geographic.id,
            "Error on parsing geographic Coverage"
        )
        self.assertEqual(
            "3",
            coverage.temporal.id,
            "Error on parsing geographic Coverage"
        )
        self.assertEqual(
            "4",
            coverage.taxonomic.id,
            "Error on parsing geographic Coverage"
        )
        self.assertFalse(
            coverage.referencing,
            "Error on parsing referencing"
        )
        self.assertEqualTree(et.fromstring(xml_text), coverage.to_element(), "Creator error on to element")

    def test_parse_referencing(self):
        xml_text = """
<coverage>
    <references>1</references>
</coverage>
        """
        coverage = EMLCoverage.from_string(xml_text)
        self.assertEqual("1", coverage.id, "Error on parsing id")
        self.assertTrue(
            coverage.referencing,
            "Error on parsing referencing"
        )
        self.assertEqualTree(et.fromstring(xml_text), coverage.to_element(), "Creator error on to element")

    def test_parse_invalid(self):
        self.assertRaises(
            TypeError,
            EMLCoverage.from_string,
            "<coverage></coverage>"
        )


if __name__ == '__main__':
    unittest.main()
