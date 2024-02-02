import unittest

from lxml import etree as et

from dwca.utils import Language
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
        variable = IndividualName("Saez", first_name="Juan", salutation="MSc", language=Language.ESP)
        self.assertEqual("Saez, J. MSc.", str(variable), "Not equal to string")
        self.assertEqual(
            "<Individual Name {Last Name: Saez [esp], First Name: Juan [esp], Salutation: MSc [esp]}>",
            repr(variable),
            "Not equal to string"
        )
        self.assertEqual(Language.ESP, variable.last_name.language, "Language set incorrectly")
        self.assertEqual(Language.ESP, variable.first_name[0].language, "Language set incorrectly")
        self.assertEqual(Language.ESP, variable.salutation[0].language, "Language set incorrectly")

    def test_individual_name_multi_language(self):
        variable = IndividualName(
            "Saez", first_name=[
                I18nString("Juan", "eng"),
                I18nString("Juan", "esp")
            ], salutation=[
                I18nString("MSc", "eng"),
                I18nString("Don", "esp")
            ]
        )
        self.assertRaises(ValueError, str, variable)
        self.assertEqual("Saez, J. MSc.", variable.lang(Language.ENG), "Not equal to string")
        self.assertEqual("Saez, J. Don.", variable.lang(Language.ESP), "Not equal to string")
        self.assertEqual(
            "<Individual Name {Last Name: Saez [eng], "
            "First Name: Juan [eng]/Juan [esp], "
            "Salutation: MSc [eng]/Don [esp]}>",
            repr(variable),
            "Not equal to string"
        )
        self.assertEqual(Language.ENG, variable.last_name.language, "Language set incorrectly")
        self.assertCountEqual(
            [Language.ENG, Language.ESP],
            [first_name.language for first_name in variable.first_name],
            "Language set incorrectly"
        )
        self.assertCountEqual(
            [Language.ENG, Language.ESP],
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
    <givenName xml:lang="esp">Juan</givenName>
    <salutation xml:lang="esp">MSc</salutation>
</individualName>
        """
        variable = IndividualName.from_string(example_xml)
        self.assertRaises(ValueError, str, variable)
        self.assertEqual("Saez", variable.lang(Language.ENG), "Not equal to string")
        self.assertEqual("Saez, J. MSc.", variable.lang(Language.ESP), "Not equal to string")
        self.assertEqual(Language.ENG, variable.last_name.language, "Language set incorrectly")
        self.assertEqual(Language.ESP, variable.first_name[0].language, "Language set incorrectly")
        self.assertEqual(Language.ESP, variable.salutation[0].language, "Language set incorrectly")

    def test_to_element(self):
        variable = IndividualName("Saez", language=Language.ESP)
        expected = et.Element("individualName")
        sur_name = et.Element("surName")
        sur_name.text = "Saez"
        sur_name.set("{http://www.w3.org/XML/1998/namespace}lang", "esp")
        expected.append(sur_name)
        self.assertEqualTree(expected, variable.to_element(), "Error on element")
    
    def test_to_element_complete(self):
        variable = IndividualName("Saez", first_name="Juan", salutation="Don", language=Language.ESP)
        expected = et.Element("individualName")
        sur_name = et.Element("surName")
        sur_name.text = "Saez"
        sur_name.set("{http://www.w3.org/XML/1998/namespace}lang", "esp")
        expected.append(sur_name)
        first_name = et.Element("givenName")
        first_name.text = "Juan"
        first_name.set("{http://www.w3.org/XML/1998/namespace}lang", "esp")
        expected.append(first_name)
        salutation = et.Element("salutation")
        salutation.text = "Don"
        salutation.set("{http://www.w3.org/XML/1998/namespace}lang", "esp")
        expected.append(salutation)
        self.assertEqualTree(expected, variable.to_element(), "Error on complete element")

    def test_to_element_multilanguage(self):
        variable = IndividualName(
            "Saez",
            first_name=[
                I18nString("Juan", Language.ESP),
                I18nString("John", Language.ENG),
            ],
            salutation=[
                I18nString("Don", Language.ESP),
                I18nString("Mr.", Language.ENG),
            ],
            language=Language.ESP
        )
        expected = et.Element("individualName")
        sur_name = et.Element("surName")
        sur_name.text = "Saez"
        sur_name.set("{http://www.w3.org/XML/1998/namespace}lang", "esp")
        expected.append(sur_name)
        first_name_1 = et.Element("givenName")
        first_name_1.text = "Juan"
        first_name_1.set("{http://www.w3.org/XML/1998/namespace}lang", "esp")
        expected.append(first_name_1)
        first_name_2 = et.Element("givenName")
        first_name_2.text = "John"
        first_name_2.set("{http://www.w3.org/XML/1998/namespace}lang", "eng")
        expected.append(first_name_2)
        salutation_1 = et.Element("salutation")
        salutation_1.text = "Don"
        salutation_1.set("{http://www.w3.org/XML/1998/namespace}lang", "esp")
        expected.append(salutation_1)
        salutation_2 = et.Element("salutation")
        salutation_2.text = "Mr."
        salutation_2.set("{http://www.w3.org/XML/1998/namespace}lang", "eng")
        expected.append(salutation_2)
        self.assertEqualTree(expected, variable.to_element(), "Error on multilanguage element")

    def test_lang(self):
        variable = IndividualName("Saez")
        self.assertRaises(AssertionError, variable.lang, Language.ESP)
        self.assertEqual("Saez", variable.lang(Language.ENG), "Error on simple call to lang")


if __name__ == '__main__':
    unittest.main()
