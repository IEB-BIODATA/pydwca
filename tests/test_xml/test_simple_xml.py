import unittest
from typing import Dict

from lxml import etree as et

from test_xml.test_xml import TestXML
from xml_common import XMLObject


class TestSimpleXML(TestXML):

    class SimpleXML(XMLObject):
        PRINCIPAL_TAG = "simple"

        def __init__(self, an_attribute: str, another_attribute: str) -> None:
            super().__init__()
            self.__an_attribute__ = an_attribute
            self.__another_attribute__ = another_attribute
            return

        @classmethod
        def parse(cls, element: et.Element, nmap: Dict) -> XMLObject | None:
            an_attribute = element.find("anAttribute")
            another_attribute = element.find("anotherAttribute")
            simple = TestSimpleXML.SimpleXML(
                an_attribute.text, another_attribute.text
            )
            simple.__namespace__ = nmap
            return simple

        def to_element(self) -> et.Element:
            simple_element = et.Element(self.PRINCIPAL_TAG)
            an_attribute = et.Element("anAttribute")
            an_attribute.text = self.__an_attribute__
            simple_element.append(an_attribute)
            another_attribute = et.Element("anotherAttribute")
            another_attribute.text = self.__another_attribute__
            simple_element.append(another_attribute)
            return simple_element

    def test_parse(self) -> None:
        simple_xml = """
<simple>
    <anAttribute>123</anAttribute>
    <anotherAttribute>456</anotherAttribute>
</simple>
        """
        simple = TestSimpleXML.SimpleXML.from_string(simple_xml)
        self.assertEqual(
            "123", simple.__an_attribute__, "Error on parsing `an attribute`."
        )
        self.assertEqual(
            "456", simple.__another_attribute__, "Error on parsing `another attribute`."
        )
        self.assertEqualTree(et.fromstring(simple_xml), simple.to_element(), "Error on `to_element`.")

    def test_repr(self):
        simple = TestSimpleXML.SimpleXML("an_attribute", "another_attribute")
        self.assertEqual(
            "<XMLObject tag=simple>",
            repr(simple),
            "Incorrect representation"
        )
        self.assertEqual(
            "<XMLObject tag=simple>",
            f"{simple}",
            "Incorrect representation"
        )


if __name__ == '__main__':
    unittest.main()
