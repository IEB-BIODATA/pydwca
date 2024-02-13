import unittest
from lxml import etree as et

from dwca.utils import Language
from eml.types import I18nString, ExtensionString
from test_xml.test_xml import TestXML


class TestI18nString(TestXML):
    def test_i18n_string(self):
        variable = I18nString("My variable")
        self.assertEqual("My variable", variable, "Not equal to string")
        self.assertEqual("My variable", str(variable), "Not equal to string")
        self.assertEqual("<i18n String (My variable) [eng]>", repr(variable), "Not equal to string")
        self.assertEqual(Language.ENG, variable.language, "Language set incorrectly")

    def test_i18n_spanish(self):
        variable = I18nString("Mi variable", lang=Language.ESP)
        self.assertEqual("Mi variable", variable, "Not equal to string")
        self.assertEqual("Mi variable", str(variable), "Not equal to string")
        self.assertEqual("<i18n String (Mi variable) [esp]>", repr(variable), "Not equal to string")
        self.assertEqual(Language.ESP, variable.language, "Language set incorrectly")

    def test_parse(self):
        self.assertIsNone(I18nString.parse(None, {}), "Parsing something")
        example_xml = """
<title
    xml:lang="eng"
>My variable</title>
        """
        variable = I18nString.from_string(example_xml)
        self.assertEqual("My variable", variable, "Not equal to string")
        self.assertEqual(Language.ENG, variable.language, "Language set incorrectly")

    def test_wrong_language_type(self):
        self.assertRaises(
            TypeError, I18nString, "My variable", 20
        )

    def test_to_element(self):
        variable = I18nString("Mi variable", lang=Language.ESP)
        self.assertRaises(RuntimeError, variable.to_element)
        variable.set_tag("title")
        expected = et.Element("title")
        expected.text = "Mi variable"
        expected.set("{http://www.w3.org/XML/1998/namespace}lang", "esp")
        self.assertEqualTree(expected, variable.to_element(), "Error on element")

    def test_equal(self):
        variable = I18nString("My variable")
        self.assertEqual(I18nString("My variable"), variable, "Error on equal implementation")
        self.assertNotEqual(
            I18nString("My variable", lang=Language.ESP),
            variable,
            "Error on equal implementation"
        )

    def test_not_equal(self):
        variable = I18nString("My variable")
        self.assertNotEqual(ExtensionString("My variable"), variable, "Error on equal implementation")
        self.assertNotEqual(I18nString("Another variable"), variable, "Error on equal implementation")
        self.assertNotEqual(30, variable, "Error on equal implementation")

    def test_wrong_language(self):
        self.assertRaises(
            NotImplementedError, I18nString, "My variable", "6f5"
        )
        self.assertRaises(
            NotImplementedError, I18nString, "My variable", "de"
        )
        self.assertRaises(
            NotImplementedError, I18nString, "My variable", "fr"
        )


if __name__ == '__main__':
    unittest.main()
