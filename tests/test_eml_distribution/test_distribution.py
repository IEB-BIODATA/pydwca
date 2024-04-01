import unittest

from lxml import etree as et

from eml.resources import EMLDistribution
from eml.resources.distribution import EMLOnline, EMLOffline
from test_xml.test_xml import TestXML


class TestDistribution(TestXML):
    DEFAULT_TAGS = {
        "scope": "document",
        "function": "download",
    }

    def test_parse_none(self):
        self.assertIsNone(EMLDistribution.parse(None, {}), "Distribution from nowhere")

    def test_no_argument(self):
        self.assertRaises(
            TypeError,
            EMLDistribution,
        )

    def test_multiple_distribution(self):
        self.assertRaises(
            TypeError,
            EMLDistribution,
            online=EMLOnline(),
            offline=EMLOffline("Tape, 3.5 inch Floppy Disk, hardcopy"),
        )

    def test_parse_online(self):
        xml_text = """
<distribution id="1" scope="document">
    <online>
        <url>http://data.org/getdata?id=98332</url>
    </online>
</distribution>
        """
        distribution = EMLDistribution.from_string(xml_text)
        self.assertEqual("1", distribution.id, "Error on parsing id")
        self.assertEqual(
            "http://data.org/getdata?id=98332",
            distribution.online.url,
            "Error on parsing online"
        )
        self.assertEqualTree(et.fromstring(xml_text), distribution.to_element(), "Creator error on to element")

    def test_parse_offline(self):
        xml_text = """
<distribution id="1" scope="document">
    <offline>
        <mediumName>Tape, 3.5 inch Floppy Disk, hardcopy</mediumName>
    </offline>
</distribution>
        """
        distribution = EMLDistribution.from_string(xml_text)
        self.assertEqual("1", distribution.id, "Error on parsing id")
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
