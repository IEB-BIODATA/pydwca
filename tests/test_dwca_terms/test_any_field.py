import unittest

from lxml import etree as et

from dwca.terms import MeasurementValue
from test_xml.test_xml import TestXML


class TestAnyField(TestXML):
    def test_parse(self):
        measurement_value_xml = """<field index="3" term="http://rs.tdwg.org/dwc/terms/measurementValue"/>"""
        measurement_value = MeasurementValue.from_string(measurement_value_xml)
        self.assertEqual(
            "http://rs.tdwg.org/dwc/terms/measurementValue",
            measurement_value.uri,
            "Wrong URI"
        )
        self.assertEqual(3, measurement_value.index, "Wrong index")
        self.assertEqualTree(et.fromstring(measurement_value_xml), measurement_value.to_element(), "Wrong generated element.")
        pass

    def test_format(self):
        measurement_value = MeasurementValue(3)
        value = "1"
        with self.assertWarnsRegex(Warning, "<Any>"):
            self.assertEqual(
                value, measurement_value.format(value), "Error formatting Any"
            )
        value = "14.5"
        with self.assertWarnsRegex(Warning, "<Any>"):
            self.assertEqual(
                value, measurement_value.format(value), "Error formatting Any"
            )
        value = "UV-light"
        with self.assertWarnsRegex(Warning, "<Any>"):
            self.assertEqual(value, measurement_value.format(value), "Error formatting Any")


if __name__ == '__main__':
    unittest.main()
