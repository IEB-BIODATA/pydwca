import unittest

from lxml import etree as et

from dwca.utils import Language
from test_xml.test_xml import TestXML
from eml.types import OrganizationName


class TestOrganizationName(TestXML):
    def test_organization_name(self):
        variable = OrganizationName("Institute of Ecology and Biodiversity")
        self.assertEqual("Institute of Ecology and Biodiversity", variable, "Not equal to string")
        self.assertEqual("Institute of Ecology and Biodiversity", str(variable), "Not equal to string")
        self.assertEqual(
            "<Organization Name (Institute of Ecology and Biodiversity) [eng]>",
            repr(variable),
            "Not equal to string"
        )
        self.assertEqual(Language.ENG, variable.language, "Language set incorrectly")

    def test_organization_name_spanish(self):
        variable = OrganizationName("Instituto de Ecología y Biodiversidad", lang=Language.ESP)
        self.assertEqual("Instituto de Ecología y Biodiversidad", variable, "Not equal to string")
        self.assertEqual("Instituto de Ecología y Biodiversidad", str(variable), "Not equal to string")
        self.assertEqual(
            "<Organization Name (Instituto de Ecología y Biodiversidad) [esp]>",
            repr(variable),
            "Not equal to string"
        )
        self.assertEqual(Language.ESP, variable.language, "Language set incorrectly")

    def test_parse(self):
        self.assertIsNone(OrganizationName.parse(None, {}), "Parsing something")
        example_xml = """
<organizationName
    xml:lang="eng"
>Institute of Ecology and Biodiversity</organizationName>
        """
        variable = OrganizationName.from_string(example_xml)
        self.assertEqual("Institute of Ecology and Biodiversity", variable, "Not equal to string")
        self.assertEqual(Language.ENG, variable.language, "Language set incorrectly")

    def test_wrong_language_type(self):
        self.assertRaises(
            TypeError, OrganizationName, "My variable", 20
        )

    def test_to_element(self):
        variable = OrganizationName("Instituto de Ecología y Biodiversidad", lang=Language.ESP)
        expected = et.Element("organizationName")
        expected.text = "Instituto de Ecología y Biodiversidad"
        expected.set("{http://www.w3.org/XML/1998/namespace}lang", "esp")
        self.assertEqualTree(expected, variable.to_element(), "Error on element")
        variable.set_tag("AnInvalidTag")
        self.assertEqualTree(expected, variable.to_element(), "Error on element")


if __name__ == '__main__':
    unittest.main()
