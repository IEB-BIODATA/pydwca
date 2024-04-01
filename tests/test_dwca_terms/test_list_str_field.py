import unittest

from lxml import etree as et

from dwca.terms import HigherClassification
from test_xml.test_xml import TestXML


class TestListStringField(TestXML):
    def test_parse(self):
        higher_class_xml = """<field index="3" term="http://rs.tdwg.org/dwc/terms/higherClassification"/>"""
        decimal = HigherClassification.from_string(higher_class_xml)
        self.assertEqual(
            "http://rs.tdwg.org/dwc/terms/higherClassification",
            decimal.uri,
            "Wrong URI"
        )
        self.assertEqual(3, decimal.index, "Wrong index")
        self.assertEqualTree(et.fromstring(higher_class_xml), decimal.to_element(), "Wrong generated element.")
        pass

    def test_format(self):
        higher_classification = HigherClassification(3)
        value = "Plantae | Magnoliophyta | Magnoliopsida | Canellales | Winteraceae | Drimys"
        self.assertEqual(
            6, len(higher_classification.format(value)), "Error formatting list of string"
        )
        self.assertEqual(
            ["Plantae", "Magnoliophyta", "Magnoliopsida", "Canellales", "Winteraceae", "Drimys"],
            higher_classification.format(value), "Error formatting list of string"
        )
        value = ""
        self.assertEqual(
            1, len(higher_classification.format(value)), "Error formatting list of string"
        )
        self.assertEqual(
            [""],
            higher_classification.format(value), "Error formatting list of string"
        )


if __name__ == '__main__':
    unittest.main()
