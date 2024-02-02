import unittest

from lxml import etree as et

from eml.resources import EMLLicense
from test_xml.test_xml import TestXML


class TestLicence(TestXML):
    def test_parse_simple(self):
        text_xml = """
<licensed>
    <licenseName>Apache License 2.0</licenseName>
</licensed>
        """
        licence = EMLLicense.from_string(text_xml)
        self.assertEqual("Apache License 2.0", licence.name, "Error on parsing name")
        self.assertIsNone(licence.url, "Error on parsing url")
        self.assertIsNone(licence.id, "Error on parsing identifier")
        self.assertEqualTree(et.fromstring(text_xml), licence.to_element(), "Error on to element")

    def test_parse_empty_name(self):
        text_xml = """
<licensed>
    <licenseName/>
</licensed>
        """
        licence = EMLLicense.from_string(text_xml)
        self.assertEqual("", licence.name, "Error on parsing name")
        self.assertIsNone(licence.url, "Error on parsing url")
        self.assertIsNone(licence.id, "Error on parsing identifier")
        self.assertEqualTree(et.fromstring(text_xml), licence.to_element(), "Error on to element")

    def test_parse_complete(self):
        text_xml = """
<licensed>
    <licenseName>Apache License 2.0</licenseName>
    <url>https://spdx.org/licenses/Apache-2.0.html</url>
    <identifier>Apache-2.0</identifier>
</licensed>
        """
        licence = EMLLicense.from_string(text_xml)
        self.assertEqual("Apache License 2.0", licence.name, "Error on parsing name")
        self.assertEqual("https://spdx.org/licenses/Apache-2.0.html", licence.url, "Error on parsing url")
        self.assertEqual("Apache-2.0", licence.id, "Error on parsing identifier")
        self.assertEqualTree(et.fromstring(text_xml), licence.to_element(), "Error on to element")

    def test_parse_none(self):
        self.assertIsNone(EMLLicense.parse(None, {}), "Licence parsed from nowhere")


if __name__ == '__main__':
    unittest.main()
