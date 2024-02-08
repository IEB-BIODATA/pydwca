import unittest

from lxml import etree as et

from eml.types import ExtensionURI
from test_xml.test_xml import TestXML


class TestExtensionURI(TestXML):
    def test_extension(self):
        variable = ExtensionURI("http://a_link.org", "A label")
        self.assertEqual("http://a_link.org", variable, "Not equal to string")
        self.assertEqual("http://a_link.org", str(variable), "Not equal to string")
        self.assertEqual(
            "<ExtensionURI (http://a_link.org [label=A label])>",
            repr(variable), "Not equal to string"
        )
        self.assertEqual("A label", variable.label, "Label set incorrectly")

    def test_valid_uri(self):
        self.assertRaises(
            ValueError, ExtensionURI, "An invalid URL", "A label"
        )

    def test_parse(self):
        self.assertIsNone(ExtensionURI.parse(None, {}), "Parsing something")
        example_xml = """
<propertyURI
    label="A label"
>http://a_link.org</propertyURI>
        """
        variable = ExtensionURI.from_string(example_xml)
        self.assertEqual("http://a_link.org", variable, "Not equal to string")
        self.assertIsNotNone(variable.label, "Label set incorrectly")
        self.assertEqual("A label", variable.label, "Label set incorrectly")

    def test_to_element(self):
        variable = ExtensionURI("http://a_link.org", "A label")
        self.assertRaises(RuntimeError, variable.to_element)
        variable.set_tag("propertyURI")
        expected = et.Element("propertyURI")
        expected.set("label", "A label")
        expected.text = "http://a_link.org"
        self.assertEqualTree(expected, variable.to_element(), "Error on element")

    def test_equal(self):
        variable = ExtensionURI("http://a_link.org", "A label")
        self.assertEqual("http://a_link.org", variable, "Error on equal implementation")
        self.assertEqual(ExtensionURI("http://a_link.org", "A label"), variable, "Error on equal implementation")

    def test_not_equal(self):
        variable = ExtensionURI("http://a_link.org", "A label")
        self.assertNotEqual(
            ExtensionURI("http://a_link.org", "Another label"),
            variable, "Error on equal implementation"
        )
        self.assertNotEqual(
            ExtensionURI("http://another_link.org", "A label"),
            variable, "Error on equal implementation"
        )
        self.assertNotEqual(
            ExtensionURI("http://another_link.org", "Another label"),
            variable, "Error on equal implementation"
        )
        self.assertNotEqual(30, variable, "Error on equal implementation")


if __name__ == '__main__':
    unittest.main()
