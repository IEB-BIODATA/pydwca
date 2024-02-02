import unittest

from lxml import etree as et

from dwca.utils import Language
from test_xml.test_xml import TestXML
from eml.types import PositionName


class TestPositionName(TestXML):
    def test_position_name(self):
        variable = PositionName("IEB - BIODATA Computer Researcher")
        self.assertEqual("IEB - BIODATA Computer Researcher", variable, "Not equal to string")
        self.assertEqual("IEB - BIODATA Computer Researcher", str(variable), "Not equal to string")
        self.assertEqual(
            "<Position Name (IEB - BIODATA Computer Researcher) [eng]>",
            repr(variable),
            "Not equal to string"
        )
        self.assertEqual(Language.ENG, variable.language, "Language set incorrectly")

    def test_organization_name_spanish(self):
        variable = PositionName("IEB - BIODATA Investigador Informático", lang=Language.ESP)
        self.assertEqual("IEB - BIODATA Investigador Informático", variable, "Not equal to string")
        self.assertEqual("IEB - BIODATA Investigador Informático", str(variable), "Not equal to string")
        self.assertEqual(
            "<Position Name (IEB - BIODATA Investigador Informático) [esp]>",
            repr(variable),
            "Not equal to string"
        )
        self.assertEqual(Language.ESP, variable.language, "Language set incorrectly")

    def test_parse(self):
        self.assertIsNone(PositionName.parse(None, {}), "Parsing something")
        example_xml = """
<positionName
    xml:lang="eng"
>IEB - BIODATA Computer Researcher</positionName>
        """
        variable = PositionName.from_string(example_xml)
        self.assertEqual("IEB - BIODATA Computer Researcher", variable, "Not equal to string")
        self.assertEqual(Language.ENG, variable.language, "Language set incorrectly")

    def test_wrong_language_type(self):
        self.assertRaises(
            TypeError, PositionName, "My variable", 20
        )

    def test_to_element(self):
        variable = PositionName("IEB - BIODATA Investigador Informático", lang=Language.ESP)
        expected = et.Element("positionName")
        expected.text = "IEB - BIODATA Investigador Informático"
        expected.set("{http://www.w3.org/XML/1998/namespace}lang", "esp")
        self.assertEqualTree(expected, variable.to_element(), "Error on element")
        variable.set_tag("AnInvalidTag")
        self.assertEqualTree(expected, variable.to_element(), "Error on element")


if __name__ == '__main__':
    unittest.main()
