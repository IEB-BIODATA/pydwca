import unittest

from lxml import etree as et

from dwca.terms import DecimalLatitude
from test_xml.test_xml import TestXML


class TestFloatField(TestXML):
    def test_parse(self):
        decimal_xml = """<field index="3" term="http://rs.tdwg.org/dwc/terms/decimalLatitude"/>"""
        decimal = DecimalLatitude.from_string(decimal_xml)
        self.assertEqual(
            "http://rs.tdwg.org/dwc/terms/decimalLatitude",
            decimal.uri,
            "Wrong URI"
        )
        self.assertEqual(3, decimal.index, "Wrong index")
        self.assertEqualTree(et.fromstring(decimal_xml), decimal.to_element(), "Wrong generated element.")
        pass

    def test_format(self):
        decimal = DecimalLatitude(3)
        value = "92.0"
        self.assertGreaterEqual(
            1e-10, abs(decimal.format(value) - 92.0), "Error formatting float"
        )
        value = "18.00005"
        self.assertGreaterEqual(
            1e-10, abs(decimal.format(value) - 18.00005), "Error formatting float"
        )
        value = "Invalid float"
        self.assertIsNone(decimal.format(value), "Error formatting invalid float")


if __name__ == '__main__':
    unittest.main()
