import unittest

from lxml import etree as et

from eml.resources import EMLDistribution
from test_xml.test_xml import TestXML


class TestDistribution(TestXML):
    DEFAULT_TAGS = {
        "scope": "document",
        "function": "download",
    }

    def test_parse_none(self):
        self.assertIsNone(EMLDistribution.parse(None, {}), "Distribution from nowhere")

    def test_parse(self):
        xml_text = """
<distribution id="1" scope="document">
    <online>
        <url>http://data.org/getdata?id=98332</url>
    </online>
    <offline>
        <mediumName>Tape, 3.5 inch Floppy Disk, hardcopy</mediumName>
    </offline>
</distribution>
        """
        distribution = EMLDistribution.from_string(xml_text)
        self.assertEqual("1", distribution.id, "Error on parsing id")
        self.assertEqual(
            "http://data.org/getdata?id=98332",
            distribution.online.url,
            "Error on parsing online"
        )
        self.assertEqual(
            "Tape, 3.5 inch Floppy Disk, hardcopy",
            distribution.offline.medium_name,
            "Error on parsing offline"
        )
        self.assertEqualTree(et.fromstring(xml_text), distribution.to_element(), "Creator error on to element")

    def test_parse_referencing(self):
        xml_text = """
<distribution>
    <references>1</references>
</distribution>
        """
        distribution = EMLDistribution.from_string(xml_text)
        self.assertEqual("1", distribution.id, "Error on parsing id")
        self.assertTrue(
            distribution.referencing,
            "Error on parsing referencing"
        )
        self.assertEqualTree(et.fromstring(xml_text), distribution.to_element(), "Creator error on to element")


if __name__ == '__main__':
    unittest.main()
