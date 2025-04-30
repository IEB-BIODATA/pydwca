import unittest

from lxml import etree as et

from xml_common.utils import Language
from test_xml.test_xml import TestXML
from eml.types import IndividualName, I18nString


class TestPerson(TestXML):
    def test_individual_name_last_name(self):
        variable = IndividualName("Saez")
        self.assertEqual("Saez", str(variable), "Not equal to string")
        self.assertEqual(
            "<Individual Name {Last Name: Saez [eng]}>",
            repr(variable),
            "Not equal to string"
        )
        self.assertEqual(Language.ENG, variable.last_name.language, "Language set incorrectly")

    def test_individual_name_first_name(self):
        variable = IndividualName("Saez", first_name="Juan")
        self.assertEqual("Saez, J.", str(variable), "Not equal to string")
        self.assertEqual(
            "<Individual Name {Last Name: Saez [eng], First Name: Juan [eng]}>",
            repr(variable),
            "Not equal to string"
        )
        self.assertEqual(Language.ENG, variable.last_name.language, "Language set incorrectly")
        self.assertEqual(Language.ENG, variable.first_name[0].language, "Language set incorrectly")

    def test_individual_name_salutation(self):
        variable = IndividualName("Saez", first_name="Juan", salutation="MSc")
        self.assertEqual("Saez, J. MSc.", str(variable), "Not equal to string")
        self.assertEqual(
            "<Individual Name {Last Name: Saez [eng], First Name: Juan [eng], Salutation: MSc [eng]}>",
            repr(variable),
            "Not equal to string"
        )
        self.assertEqual(Language.ENG, variable.last_name.language, "Language set incorrectly")
        self.assertEqual(Language.ENG, variable.first_name[0].language, "Language set incorrectly")
        self.assertEqual(Language.ENG, variable.salutation[0].language, "Language set incorrectly")

    def test_individual_name_spanish(self):
        variable = IndividualName("Saez", first_name="Juan", salutation="MSc", language=Language.SPA)
        self.assertEqual("Saez, J. MSc.", str(variable), "Not equal to string")
        self.assertEqual(
            "<Individual Name {Last Name: Saez [spa], First Name: Juan [spa], Salutation: MSc [spa]}>",
            repr(variable),
            "Not equal to string"
        )
        self.assertEqual(Language.SPA, variable.last_name.language, "Language set incorrectly")
        self.assertEqual(Language.SPA, variable.first_name[0].language, "Language set incorrectly")
        self.assertEqual(Language.SPA, variable.salutation[0].language, "Language set incorrectly")

    def test_individual_name_multi_language(self):
        variable = IndividualName(
            "Saez", first_name=[
                I18nString("Juan", "eng"),
                I18nString("Juan", "spa")
            ], salutation=[
                I18nString("MSc", "eng"),
                I18nString("Don", "spa")
            ]
        )
        self.assertRaises(ValueError, str, variable)
        self.assertEqual("Saez, J. MSc.", variable.lang(Language.ENG), "Not equal to string")
        self.assertEqual("Saez, J. Don.", variable.lang(Language.SPA), "Not equal to string")
        self.assertEqual(
            "<Individual Name {Last Name: Saez [eng], "
            "First Name: Juan [eng]/Juan [spa], "
            "Salutation: MSc [eng]/Don [spa]}>",
            repr(variable),
            "Not equal to string"
        )
        self.assertEqual(Language.ENG, variable.last_name.language, "Language set incorrectly")
        self.assertCountEqual(
            [Language.ENG, Language.SPA],
            [first_name.language for first_name in variable.first_name],
            "Language set incorrectly"
        )
        self.assertCountEqual(
            [Language.ENG, Language.SPA],
            [salutation.language for salutation in variable.salutation],
            "Language set incorrectly"
        )

    def test_parse(self):
        self.assertIsNone(IndividualName.parse(None, {}), "Parsing something")
        example_xml = """
<individualName>
    <surName>Saez</surName>
</individualName>
        """
        variable = IndividualName.from_string(example_xml)
        self.assertEqual("Saez", str(variable), "Not equal to string")
        self.assertEqual(Language.ENG, variable.last_name.language, "Language set incorrectly")

    def test_parse_complete(self):
        self.assertIsNone(IndividualName.parse(None, {}), "Parsing something")
        example_xml = """
<individualName>
    <surName>Saez</surName>
    <givenName xml:lang="spa">Juan</givenName>
    <salutation xml:lang="spa">MSc</salutation>
</individualName>
        """
        variable = IndividualName.from_string(example_xml)
        self.assertRaises(ValueError, str, variable)
        self.assertEqual("Saez", variable.lang(Language.ENG), "Not equal to string")
        self.assertEqual("Saez, J. MSc.", variable.lang(Language.SPA), "Not equal to string")
        self.assertEqual(Language.ENG, variable.last_name.language, "Language set incorrectly")
        self.assertEqual(Language.SPA, variable.first_name[0].language, "Language set incorrectly")
        self.assertEqual(Language.SPA, variable.salutation[0].language, "Language set incorrectly")

    def test_to_element(self):
        variable = IndividualName("Saez", language=Language.SPA)
        expected = et.Element("individualName")
        sur_name = et.Element("surName")
        sur_name.text = "Saez"
        sur_name.set("{http://www.w3.org/XML/1998/namespace}lang", "spa")
        expected.append(sur_name)
        self.assertEqualTree(expected, variable.to_element(), "Error on element")
    
    def test_to_element_complete(self):
        variable = IndividualName("Saez", first_name="Juan", salutation="Don", language=Language.SPA)
        expected = et.Element("individualName")
        sur_name = et.Element("surName")
        sur_name.text = "Saez"
        sur_name.set("{http://www.w3.org/XML/1998/namespace}lang", "spa")
        expected.append(sur_name)
        first_name = et.Element("givenName")
        first_name.text = "Juan"
        first_name.set("{http://www.w3.org/XML/1998/namespace}lang", "spa")
        expected.append(first_name)
        salutation = et.Element("salutation")
        salutation.text = "Don"
        salutation.set("{http://www.w3.org/XML/1998/namespace}lang", "spa")
        expected.append(salutation)
        self.assertEqualTree(expected, variable.to_element(), "Error on complete element")

    def test_to_element_multilanguage(self):
        variable = IndividualName(
            "Saez",
            first_name=[
                I18nString("Juan", Language.SPA),
                I18nString("John", Language.ENG),
            ],
            salutation=[
                I18nString("Don", Language.SPA),
                I18nString("Mr.", Language.ENG),
            ],
            language=Language.SPA
        )
        expected = et.Element("individualName")
        sur_name = et.Element("surName")
        sur_name.text = "Saez"
        sur_name.set("{http://www.w3.org/XML/1998/namespace}lang", "spa")
        expected.append(sur_name)
        first_name_1 = et.Element("givenName")
        first_name_1.text = "Juan"
        first_name_1.set("{http://www.w3.org/XML/1998/namespace}lang", "spa")
        expected.append(first_name_1)
        first_name_2 = et.Element("givenName")
        first_name_2.text = "John"
        first_name_2.set("{http://www.w3.org/XML/1998/namespace}lang", "eng")
        expected.append(first_name_2)
        salutation_1 = et.Element("salutation")
        salutation_1.text = "Don"
        salutation_1.set("{http://www.w3.org/XML/1998/namespace}lang", "spa")
        expected.append(salutation_1)
        salutation_2 = et.Element("salutation")
        salutation_2.text = "Mr."
        salutation_2.set("{http://www.w3.org/XML/1998/namespace}lang", "eng")
        expected.append(salutation_2)
        self.assertEqualTree(expected, variable.to_element(), "Error on multilanguage element")

    def test_lang(self):
        variable = IndividualName("Saez")
        self.assertRaises(AssertionError, variable.lang, Language.SPA)
        self.assertEqual("Saez", variable.lang(Language.ENG), "Error on simple call to lang")


if __name__ == '__main__':
    unittest.main()
