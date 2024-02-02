import unittest
from lxml import etree as et
from eml.types import ExtensionString
from test_xml.test_xml import TestXML


class TestExtensionString(TestXML):
    def test_extension(self):
        variable = ExtensionString("My variable")
        self.assertEqual("My variable", variable, "Not equal to string")
        self.assertEqual("My variable", str(variable), "Not equal to string")
        self.assertEqual("<ExtensionString (My variable)>", repr(variable), "Not equal to string")
        self.assertIsNone(variable.system, "System set incorrectly")

    def test_extension_system(self):
        variable = ExtensionString("My variable", system="http://gbif.org")
        self.assertEqual("My variable", variable, "Not equal to string")
        self.assertEqual(
            "<ExtensionString system='http://gbif.org' (My variable)>",
            repr(variable),
            "Not equal to string"
        )
        self.assertIsNotNone(variable.system, "System set incorrectly")
        self.assertEqual("http://gbif.org", variable.system, "System set incorrectly")

    def test_parse(self):
        self.assertIsNone(ExtensionString.parse(None, {}), "Parsing something")
        example_xml = """
<alternativeIdentifier
    system="http://gbif.org"
>My variable</alternativeIdentifier>
        """
        variable = ExtensionString.from_string(example_xml)
        self.assertEqual("My variable", variable, "Not equal to string")
        self.assertIsNotNone(variable.system, "System set incorrectly")
        self.assertEqual("http://gbif.org", variable.system, "System set incorrectly")

    def test_parse_no_system(self):
        example_xml = """
<alternativeIdentifier>My variable</alternativeIdentifier>
        """
        variable = ExtensionString.from_string(example_xml)
        self.assertEqual("My variable", variable, "Not equal to string")
        self.assertIsNone(variable.system, "System set incorrectly")

    def test_to_element(self):
        variable = ExtensionString("My variable")
        self.assertRaises(RuntimeError, variable.to_element)
        variable.set_tag("alternativeIdentifier")
        expected = et.Element("alternativeIdentifier")
        expected.text = "My variable"
        self.assertEqualTree(expected, variable.to_element(), "Error on element")

    def test_to_element_system(self):
        variable = ExtensionString("My variable", system="A system")
        self.assertRaises(RuntimeError, variable.to_element)
        variable.set_tag("alternativeIdentifier")
        expected = et.Element("alternativeIdentifier")
        expected.text = "My variable"
        expected.set("system", "A system")
        self.assertEqualTree(expected, variable.to_element(), "Error on element")

    def test_equal(self):
        variable = ExtensionString("My variable")
        self.assertEqual(ExtensionString("My variable"), variable, "Error on equal implementation")

    def test_not_equal(self):
        variable = ExtensionString("My variable")
        self.assertNotEquals(ExtensionString("Another variable"), variable, "Error on equal implementation")
        self.assertNotEquals(30, variable, "Error on equal implementation")


if __name__ == '__main__':
    unittest.main()
